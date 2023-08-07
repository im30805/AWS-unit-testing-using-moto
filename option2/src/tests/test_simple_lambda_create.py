import json
import boto3
from moto import mock_lambda, mock_iam

@mock_lambda
@mock_iam
def test_lambda_create():
    lambda_cli = boto3.client('lambda')
    iam_cli = boto3.client('iam')

    role_arn = iam_cli.create_role(
            RoleName='foo',
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Version": "2021-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "lambda.amazonaws.com"
                            },
                            "Action": "sts:AssumeRole"
                        }
                    ]
                }
            )
        )['Role']['Arn']

    return lambda_cli.create_function(
        FunctionName='ECOM-AdminCreateProduct',
        Runtime='python3.8',
        Role=role_arn,
        Handler='ham.handler',
        Code={'ZipFile': b'bar'}
    )['FunctionArn']