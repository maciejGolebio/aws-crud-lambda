import pulumi
import pulumi_aws as aws

BOOKS_DYNAMODB_TABLE_NAME = "books"

books_dynamodb_table = aws.dynamodb.Table(
    BOOKS_DYNAMODB_TABLE_NAME,
    attributes=[
        aws.dynamodb.TableAttributeArgs(
            name="author",
            type="S",
        ),
        aws.dynamodb.TableAttributeArgs(
            name="title",
            type="S",
        )
    ],
    billing_mode="PROVISIONED",
    hash_key="title",
    range_key="author",
    read_capacity=5,
    tags={
        "Environment": "development",
        "Name": BOOKS_DYNAMODB_TABLE_NAME,
    },
    write_capacity=20
)
