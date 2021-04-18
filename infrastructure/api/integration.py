import pulumi
import pulumi_aws as aws
from infrastructure.api.api_gw import api
from infrastructure.cognito.user_pool import pool
from infrastructure.lambda_crud.function import lambda_crud

METHODS = ["GET", "POST", "PUT", "DELETE"]

methods = {}
integrations = {}

book_resource = aws.apigateway.Resource(
    "book-resource",
    rest_api=api.id,
    parent_id=api.root_resource_id,
    path_part="book")

cognito_authorizer = aws.apigateway.Authorizer(
    "cognito-authorizer",
    type="COGNITO_USER_POOLS",
    rest_api=api.id,
    provider_arns=[pool.arn]
)

for method in METHODS:
    methods[method] = aws.apigateway.Method(
        method,
        rest_api=api.id,
        resource_id=book_resource.id,
        http_method=method,
        authorization="COGNITO_USER_POOLS",
        authorizer_id=cognito_authorizer.id,
        opts=pulumi.ResourceOptions(
            depends_on=[pool, api, book_resource]
        )
    )
    integrations[method] = aws.apigateway.Integration(
        method,
        rest_api=api.id,
        resource_id=book_resource.id,
        http_method=methods[method].http_method,
        type="AWS_PROXY",
        uri=lambda_crud.invoke_arn,
        integration_http_method="POST",
        opts=pulumi.ResourceOptions(
            depends_on=[api, lambda_crud]
        )
    )

permissions = lambda_permission = aws.lambda_.Permission(
    "lambda-crud",
    action="lambda:InvokeFunction",
    function=lambda_crud.name,
    principal="apigateway.amazonaws.com",
    source_arn=api.execution_arn.apply(
        lambda execution_arn: f"{execution_arn}/*/*/*"),
    opts=pulumi.ResourceOptions(
        depends_on=[api, lambda_crud]
    )
)


