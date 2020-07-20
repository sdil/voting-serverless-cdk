from aws_cdk import core
from aws_cdk.aws_apigatewayv2 import (
    LambdaProxyIntegration,
    HttpApi,
    HttpMethod,
)
from aws_cdk.aws_lambda import Function, Runtime, Code as lambda_code


class VotingServerlessCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vote_api = HttpApi(self, "VoteHttpApi")

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

        # API Gateway (HTTP API)
        # Lambdas:
        # - GET /vote/<id>
        # - GET /
        # - POST /vote
        # - POST /vote/<id>
        # DynamoDB tables:
        # - vote
        # - aggregated_vote
        # DynamoDB Stream
        # Lambda DynamoDB Stream worker consumer
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
