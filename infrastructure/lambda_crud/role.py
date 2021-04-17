import json

import pulumi
import pulumi_aws as aws
from infrastructure.dynamodb.table import books_dynamodb_table

config = pulumi.Config()
lambda_name = config.get('lambda_name')

role = aws.iam.Role(
    lambda_name,
    name=lambda_name,
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com",
                }
            },
        ]
    }
    ),
)

policy = aws.iam.Policy(
    lambda_name,
    name=lambda_name,
    description="IAM policy for logging from a lambda and table access",
    policy=books_dynamodb_table.arn.apply(
        lambda arn: json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": [
                            "dynamodb:UpdateItem",
                            "dynamodb:PutItem",
                            "dynamodb:GetItem",
                            "dynamodb:DescribeTable"
                        ],
                        "Resource": arn,
                        "Effect": "Allow",
                    },
                    {
                        "Action": [
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents"
                        ],
                        "Resource": "arn:aws:logs:*:*:*",
                        "Effect": "Allow"
                    }
                ]
            }
        )
    )
)

role_policy_attachment = aws.iam.RolePolicyAttachment(
    lambda_name,
    role=role.name,
    policy_arn=policy.arn)
