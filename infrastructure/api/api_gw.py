import pulumi
import pulumi_aws as aws

API_NAME = "books-api"

api = aws.apigateway.RestApi(
    API_NAME,
    name=API_NAME,
    endpoint_configuration=aws.apigateway.RestApiEndpointConfigurationArgs(
        types="REGIONAL"
    ),
    description="REGIONAL BOOKS API AUTHORIZED BY COGNITO",
)

