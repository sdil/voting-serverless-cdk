from aws_cdk.aws_sqs import Queue
from aws_cdk import core
from aws_cdk.aws_apigatewayv2 import HttpApi, HttpMethod, LambdaProxyIntegration
from aws_cdk.aws_dynamodb import Attribute, AttributeType, StreamViewType, Table
from aws_cdk.aws_lambda import Function, Runtime, StartingPosition, Code
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


class VotingServerlessCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.poll_table = None
        self.aggregated_vote_table = None
        self.create_ddb_tables()

        vote_api = HttpApi(self, "VoteHttpApi")
        self.create_api_endpoints(vote_api)

        self.create_sqs_queue()

        self.users = UserPool(self, "vote-user")  # make it Hosted UI

        # Route53 pointing to api.voting.com

    def create_ddb_tables(self):
        self.poll_table = Table(
            self,
            "PollTable",
            partition_key=Attribute(name="id", type=AttributeType.STRING),
            read_capacity=10,
            write_capacity=10,
            stream=StreamViewType.NEW_IMAGE,
        )

        self.aggregated_vote_table = Table(  # Revise this
            self,
            "AggregatedVoteTable",
            partition_key=Attribute(name="id", type=AttributeType.STRING),
            read_capacity=5,
            write_capacity=5,
        )

        def setup_ddb_streams():

            # DynamoDB Lambda consumer worker
            aggregate_votes_function = Function(
                self,
                "AggregateVotesLambda",
                handler="ddb_stream.aggregate_vote_table",
                runtime=PYTHON_RUNTIME,
                code=Code.asset("./backend"),
            )

            # DynamoDB Stream (Lambda Event Source)
            self.poll_table.grant_stream_read(aggregate_votes_function)
            self.aggregated_vote_table.grant_read_write_data(aggregate_votes_function)
            ddb_aggregate_votes_event_source = DynamoEventSource(
                self.poll_table, starting_position=StartingPosition.LATEST
            )
            aggregate_votes_function.add_event_source(ddb_aggregate_votes_event_source)

        setup_ddb_streams()

    def create_api_endpoints(self, apigw):

        get_all_votes_function = api_lambda_function(
            self, "GetAllVoteLambda", "vote.get_all_votes", apigw, "/vote", GET
        )
        self.aggregated_vote_table.grant_read_data(get_all_votes_function)

        get_vote_function = api_lambda_function(
            self, "GetVoteLambda", "vote.get_vote_by_id", apigw, "/vote/{vote_id}", GET,
        )
        self.aggregated_vote_table.grant_read_data(get_vote_function)

        create_vote_function = api_lambda_function(
            self, "CreateVotePollLambda", "vote.insert_new_vote", apigw, "/vote", POST,
        )
        self.poll_table.grant_write_data(create_vote_function)

        post_vote_function = api_lambda_function(
            self, "PostVoteLambda", "vote.update_vote", apigw, "/vote/{vote_id}", POST,
        )

    def create_sqs_queue(self):

        voting_queue = Queue(self, "voting-queue")

        def create_sqs_worker():

            # SQS Consumer worker
            voting_to_ddb_function = Function(
                self,
                "VotingToDDBLambda",
                handler="sqs_worker.insert_to_vote_db_table",
                runtime=PYTHON_RUNTIME,
                code=Code.asset("./backend"),
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

        BucketDeployment(
            self,
            "DeployWithInvalidation",
            sources=[Source.asset("./frontend/dist")],
            destination_bucket=frontend_bucket,
            distribution=frontend_distribution,
            distribution_paths=["/*"],
        )

        core.CfnOutput(self, "cdn-domain", value=frontend_distribution.distribution_domain_name)

        # Route53 pointing to www.voting.com
