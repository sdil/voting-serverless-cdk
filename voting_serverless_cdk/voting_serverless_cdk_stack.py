from aws_cdk import core
from aws_cdk.aws_apigatewayv2 import (
    LambdaProxyIntegration,
    HttpApi,
    HttpMethod,
)
from aws_cdk.aws_lambda import Function, Runtime, Code as lambda_code, StartingPosition
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, StreamViewType
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsDlq


class VotingServerlessCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB
        # Poll Table
        poll_table = Table(
            self,
            "PollTable",
            partition_key=Attribute(name="id", type=AttributeType.STRING),
            read_capacity=10,
            write_capacity=10,
            stream=StreamViewType.NEW_IMAGE,
        )

        # Aggregated Vote Table
        aggregated_vote_table = Table(  # Revise this
            self,
            "AggregatedVoteTable",
            partition_key=Attribute(name="id", type=AttributeType.STRING),
            read_capacity=5,
            write_capacity=5,
        )

        # DynamoDB Lambda consumer worker
        aggregate_votes_function = Function(
            self,
            "AggregateVotesLambda",
            handler="ddb_stream.aggregate_vote_table",
            runtime=Runtime.PYTHON_3_8,
            code=lambda_code.asset("./backend"),
        )

        # DynamoDB Stream (Lambda Event Source)
        poll_table.grant_stream_read(aggregate_votes_function)
        aggregated_vote_table.grant_read_write_data(aggregate_votes_function)
        ddb_aggregate_votes_event_source = DynamoEventSource(
            poll_table, starting_position=StartingPosition.LATEST
        )
        aggregate_votes_function.add_event_source(ddb_aggregate_votes_event_source)

        # AWS API Gateway HTTP API
        vote_api = HttpApi(self, "VoteHttpApi")

        # Get Votes API
        get_all_votes_function = Function(
            self,
            "GetAllVoteLambda",
            handler="vote.get_all_votes",
            runtime=Runtime.PYTHON_3_8,
            code=lambda_code.asset("./backend"),
        )
        vote_api.add_routes(
            path="/vote",
            methods=[HttpMethod.GET],
            integration=LambdaProxyIntegration(handler=get_all_votes_function),
        )
        aggregated_vote_table.grant_read(get_all_votes_function)

        # Get Votes API
        get_vote_function = Function(
            self,
            "GetVoteLambda",
            handler="vote.get_vote_by_id",
            runtime=Runtime.PYTHON_3_8,
            code=lambda_code.asset("./backend"),
        )
        vote_api.add_routes(
            path="/vote/{vote_id}",
            methods=[HttpMethod.GET],
            integration=LambdaProxyIntegration(handler=get_vote_function),
        )
        aggregated_vote_table.grant_read(get_vote_function)

        # Create Vote API
        create_vote_function = Function(
            self,
            "CreateVotePollLambda",
            handler="vote.insert_new_vote",
            runtime=Runtime.PYTHON_3_8,
            code=lambda_code.asset("./backend"),
        )
        vote_api.add_routes(
            path="/vote",
            methods=[HttpMethod.POST],
            integration=LambdaProxyIntegration(handler=create_vote_function),
        )
        poll_table.grant_write(create_vote_function)

        # Vote a Poll API
        post_vote_function = Function(
            self,
            "PostVoteLambda",
            handler="vote.update_vote",
            runtime=Runtime.PYTHON_3_8,
            code=lambda_code.asset("./backend"),
        )
        vote_api.add_routes(
            path="/vote/{vote_id}",
            methods=[HttpMethod.POST],
            integration=LambdaProxyIntegration(handler=post_vote_function),
        )

        # API Gateway (HTTP API) DONE
        # Lambdas:
        # - GET / DONE DONE
        # - GET /vote/<id> DONE
        # - POST /vote DONE
        # - POST /vote/<id> DONE

        # DynamoDB tables: DONE
        # - vote DONE
        # - aggregated_vote DONE

        # DynamoDB Stream DONE
        # Lambda DynamoDB Stream worker consumer DONE

        # SQS queue
        # SQS Lambda consumer

        # AWS Cognito (Use Cognito Hosted UI)

        # Route53 pointing to api.voting.com


class VotingFrontendCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    # S3 Assets
    # Cloudfront serving the frontend page
    # Route53 pointing to www.voting.com
