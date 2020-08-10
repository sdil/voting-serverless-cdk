from aws_cdk.aws_sqs import Queue
from aws_cdk import core
from aws_cdk.aws_apigatewayv2 import HttpApi, HttpMethod, LambdaProxyIntegration
from aws_cdk.aws_dynamodb import (
    Attribute,
    AttributeType,
    StreamViewType,
    Table,
    ProjectionType,
)
from aws_cdk.aws_lambda import Function, Runtime, StartingPosition, Code, LayerVersion
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsDlq, SqsEventSource
from aws_cdk.aws_cognito import UserPool
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_cloudfront import (
    CloudFrontWebDistribution,
    S3OriginConfig,
    SourceConfiguration,
    Behavior,
)
from aws_cdk.aws_s3_deployment import BucketDeployment, Source
from utils import api_lambda_function

GET = HttpMethod.GET
POST = HttpMethod.POST
PYTHON_RUNTIME = Runtime.PYTHON_3_8

FRONTEND_DOMAIN_NAME = "https://vote.fadhil-blog.dev"

MAIN_PAGE_GSI = "main_page_gsi"


class VotingServerlessCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        python_deps_layer = self.create_deps_layer()

        self.poll_table = None
        self.create_ddb_tables([python_deps_layer])

        self.vote_api = self.create_api_gateway("VoteHttpApi")
        self.create_api_endpoints(self.vote_api, [python_deps_layer])

        self.create_sqs_queue([python_deps_layer])

        self.users = UserPool(self, "vote-user")  # make it Hosted UI

        # Route53 pointing to api.voting.com

    def create_api_gateway(self, name: str):
        api = HttpApi(
            self,
            name,
            cors_preflight={
                "allow_headers": ["Authorization"],
                "allow_methods": [
                    HttpMethod.GET,
                    HttpMethod.HEAD,
                    HttpMethod.OPTIONS,
                    HttpMethod.POST,
                ],
                "allow_origins": ["*"],
                "max_age": core.Duration.days(10),
            },
        )

        return api

    def create_deps_layer(self):
        """
        The packages should be stored in `python/lib/python3.7/site-packages`
        which translates to `/opt/python/lib/python3.7/site-packages` in AWS Lambda

        Refer here: https://stackoverflow.com/a/58702328/7999204
        """

        python_deps_layer = LayerVersion(
            self,
            "PythonDepsLayer",
            code=Code.from_asset("./python-deps-layer"),
            compatible_runtimes=[PYTHON_RUNTIME],
            description="A layer that contains Python Dependencies",
        )

        return python_deps_layer

    def create_ddb_tables(self, deps_layer):
        self.poll_table = Table(
            self,
            "PollTable",
            partition_key=Attribute(name="id", type=AttributeType.STRING),
            sort_key=Attribute(name="SK", type=AttributeType.STRING),
            read_capacity=10,
            write_capacity=10,
            stream=StreamViewType.NEW_IMAGE,
        )

        def setup_ddb_streams():

            # DynamoDB Lambda consumer worker
            aggregate_votes_function = Function(
                self,
                "AggregateVotesLambda",
                handler="ddb_stream.aggregate_vote_table",
                runtime=PYTHON_RUNTIME,
                code=Code.asset("./backend"),
                layers=deps_layer,
            )

            # DynamoDB Stream (Lambda Event Source)
            self.poll_table.grant_stream_read(aggregate_votes_function)
            self.poll_table.grant_read_write_data(aggregate_votes_function)
            ddb_aggregate_votes_event_source = DynamoEventSource(
                self.poll_table, starting_position=StartingPosition.LATEST
            )
            aggregate_votes_function.add_event_source(ddb_aggregate_votes_event_source)

        def setup_gsi_table():
            self.poll_table.add_global_secondary_index(
                partition_key=Attribute(name="PK2", type=AttributeType.STRING),
                projection_type=ProjectionType.INCLUDE,
                index_name=MAIN_PAGE_GSI,
                non_key_attributes=["date", "question", "result"],
            )

        setup_ddb_streams()
        setup_gsi_table()

    def create_api_endpoints(self, apigw, layers):

        get_all_votes_function = api_lambda_function(
            self,
            "GetAllVoteLambda",
            "api.get_all_votes",
            apigw,
            "/vote",
            GET,
            layers,
            [self.poll_table],
        )
        self.poll_table.grant_read_data(get_all_votes_function)

        get_vote_function = api_lambda_function(
            self,
            "GetVoteLambda",
            "api.get_vote_by_id",
            apigw,
            "/vote/{vote_id}",
            GET,
            layers,
            [self.poll_table],
        )
        self.poll_table.grant_read_data(get_vote_function)

        create_poll_function = api_lambda_function(
            self,
            "CreatePollLambda",
            "api.create_poll",
            apigw,
            "/vote",
            POST,
            layers,
            [self.poll_table],
        )
        self.poll_table.grant_write_data(create_poll_function)

        post_vote_function = api_lambda_function(
            self,
            "PostVoteLambda",
            "api.vote",
            apigw,
            "/vote/{vote_id}",
            POST,
            layers,
            [self.poll_table],
        )

    def create_sqs_queue(self, deps_layer):

        voting_queue = Queue(self, "voting-queue")

        def create_sqs_worker():

            # SQS Consumer worker
            voting_to_ddb_function = Function(
                self,
                "VotingToDDBLambda",
                handler="sqs_worker.insert_to_vote_db_table",
                runtime=PYTHON_RUNTIME,
                code=Code.asset("./backend"),
                layers=deps_layer,
            )

            # SQS Queue to Lambda trigger mapping
            voting_to_ddb_event_source = SqsEventSource(voting_queue)
            voting_to_ddb_function.add_event_source(voting_to_ddb_event_source)

        create_sqs_worker()


class VotingFrontendCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        frontend_bucket = Bucket(
            self,
            "frontend",
            website_index_document="index.html",
            public_read_access=True,
        )

        frontend_distribution = CloudFrontWebDistribution(
            self,
            "frontend-cdn",
            origin_configs=[
                SourceConfiguration(
                    s3_origin_source=S3OriginConfig(s3_bucket_source=frontend_bucket),
                    behaviors=[Behavior(is_default_behavior=True)],
                )
            ],
        )

        # CloudFront Origin should be S3 DNS name, not the S3 bucket itself
        # Otherwise, the CloudFront cannot serve dynamic pages (eg. /vote/{id} page)
        # https://stackoverflow.com/a/59359038/7999204

        BucketDeployment(
            self,
            "DeployWithInvalidation",
            sources=[Source.asset("./frontend/dist")],
            destination_bucket=frontend_bucket,
            distribution=frontend_distribution,
            distribution_paths=["/*"],
        )

        core.CfnOutput(
            self, "cdn-domain", value=frontend_distribution.distribution_domain_name
        )

        # Route53 pointing to www.voting.com
