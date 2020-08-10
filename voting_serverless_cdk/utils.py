from aws_cdk.aws_apigatewayv2 import LambdaProxyIntegration
from aws_cdk.aws_lambda import Function, Runtime, Code, Tracing
import os


def api_lambda_function(
    scope, name, handler, apigw, path, method, layer, tables, code="./backend"
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

    _lambda.add_environment("POLL_TABLE", tables[0].table_name)
    _lambda.add_environment("MAIN_PAGE_GSI", "main_page_gsi")

    apigw.add_routes(
        path=path,
        methods=[method],
        integration=LambdaProxyIntegration(handler=_lambda),
    )

    return _lambda
