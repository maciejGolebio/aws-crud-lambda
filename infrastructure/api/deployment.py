import pulumi
import pulumi_aws as aws
from infrastructure.api.api_gw import api
from infrastructure.api.integration import integrations
config = pulumi.Config()
stage_name = config.get('stage')

deployment = aws.apigateway.Deployment(
    "deployment",
    rest_api=api.id,
    stage_name="",
    opts=pulumi.ResourceOptions(depends_on=[api, *integrations.values()])
)

log_group = aws.cloudwatch.LogGroup(
    "books-api",
    retention_in_days=7
)
stage = aws.apigateway.Stage(
    stage_name,
    deployment=deployment.id,
    stage_name=stage_name,
    rest_api = api.id,
    opts=pulumi.ResourceOptions(depends_on=[log_group, api, deployment, *integrations.values()])
)
