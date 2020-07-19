from aws_cdk import core


class VotingServerlessCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    # API Gateway
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
    # AWS Cognito
    # Route53 pointing to api.voting.com

class VotingFrontendCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    # S3 Assets
    # Cloudfront serving the frontend page
    # Route53 pointing to www.voting.com
