import pulumi_aws as aws
import pulumi

from infrastructure.lambda_crud.role import role
from infrastructure.dynamodb.table import books_dynamodb_table
config = pulumi.Config()
lambda_name = config.get('lambda_name')

lambda_func = aws.lambda_.Function(
    lambda_name,
    runtime="python3.8",
    memory_size=256,
    timeout=5,
    handler="lambda.handler",
    code=pulumi.FileArchive("application/lambda_crud"),
    environment={
        "variables": {
            "TABLE": books_dynamodb_table.name,
        },
    },
    role=role.arn,
    opts=pulumi.ResourceOptions(
        depends_on=[role]
    ),
)
