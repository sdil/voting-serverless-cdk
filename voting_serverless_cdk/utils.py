from aws_cdk.aws_apigatewayv2 import LambdaProxyIntegration
from aws_cdk.aws_lambda import Function, Runtime, Code, Tracing
import os


LUMIGO_TOKEN = os.environ.get("LUMIGO_TOKEN", "")


def api_lambda_function(
    scope, name, handler, apigw, path, method, layer, code="./backend"
):
    _lambda = Function(
        scope,
        name,
        handler=handler,
        runtime=Runtime.PYTHON_3_8,
        code=Code.asset(code),
        tracing=Tracing.ACTIVE,
        layers=layer,
    )

    _lambda.add_environment("LUMIGO_TOKEN", LUMIGO_TOKEN)

    apigw.add_routes(
        path=path,
        methods=[method],
        integration=LambdaProxyIntegration(handler=_lambda),
    )

    return _lambda
