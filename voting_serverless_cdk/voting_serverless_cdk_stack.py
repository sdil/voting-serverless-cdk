from aws_cdk import core
from aws_cdk.aws_apigatewayv2 import (
    Function,
    LambdaProxyIntegration,
    HttpApi,
    HttpMethod,
)
from aws_cdk.aws_lambda import Function, Runtime, Code as lambda_code


class VotingServerlessCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        create_vote_function = Function(
            self,
            "CreateVotePollLambda",
            handler="vote.insert_new_vote",
            runtime=Runtime.PYTHON_3_8,
            code=lambda_code.asset("./backend"),
        )
        create_vote_lambda_integration = LambdaProxyIntegration(
            handler=create_vote_function
        )

        # Setup HTTP API Routes
        vote_api = HttpApi(self, "VoteHttpApi")
        vote_api.add_routes(
            path="/vote",
            methods=[HttpMethod.POST],
            integration=create_vote_lambda_integration,
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
