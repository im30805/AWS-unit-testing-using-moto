from contextlib import contextmanager
import json

@contextmanager
def create_iam_role(iam_client, role_name):
    iam_client.create_role(
        RoleName=role_name,
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

    yield



