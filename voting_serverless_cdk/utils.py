from aws_cdk import core
from aws_cdk.aws_apigatewayv2 import HttpApi, HttpMethod, LambdaProxyIntegration
from aws_cdk.aws_dynamodb import Attribute, AttributeType, StreamViewType, Table
from aws_cdk.aws_lambda import Code as lambda_code
from aws_cdk.aws_lambda import Function, Runtime, StartingPosition
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsDlq


def api_lambda_function(scope, name, handler, apigw, path, method, code="./backend"):
    _lambda = Function(
        scope,
        name,
        handler=handler,
        runtime=Runtime.PYTHON_3_8,
        code=lambda_code.asset(code),
    )

    apigw.add_routes(
        path=path,
        methods=[method],
        integration=LambdaProxyIntegration(handler=_lambda),
    )

    return _lambda
