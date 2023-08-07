import os
import boto3
import pytest
import socket
from collections import namedtuple, OrderedDict
from moto import *
from pathlib import Path
import json

# Environment variable
os.environ['AWS_DEFAULT_REGION'] = 'ap-southeast-1'

# Mocked AWS Credentials for moto, ensure this is done first
@pytest.fixture(scope='module')
def aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['POWERTOOLS_TRACE_DISABLED'] = "true"

# Fixtures which use the mock credentials
@pytest.fixture(scope='module')
def dynamodb_resource(aws_credentials):
    with mock_dynamodb2():
        yield boto3.resource('dynamodb', region_name='ap-southeast-1')
 
@pytest.fixture(scope='module')
def dynamodb_client(aws_credentials):
    with mock_dynamodb2():
       yield boto3.client('dynamodb', region_name='ap-southeast-1')

@pytest.fixture(scope='module')
def s3_resource(aws_credentials):
    with mock_s3():
        yield boto3.resource('s3', region_name='us-east-1')

@pytest.fixture(scope='module')
def s3_client(aws_credentials):
    with mock_s3():
        yield boto3.client('s3', region_name='us-east-1')

@pytest.fixture(scope='module')
def sqs_resource(aws_credentials):
    with mock_sqs():
        yield boto3.resource('sqs', region_name='ap-southeast-1')

@pytest.fixture(scope='module')
def sqs_client(aws_credentials):
    with mock_sqs():
        yield boto3.client('sqs', region_name='ap-southeast-1')

@pytest.fixture(scope='module')
def lambda_client(aws_credentials):
    with mock_lambda():
        yield boto3.client('lambda', region_name='ap-southeast-1')

@pytest.fixture(scope='module')
def iam_client(aws_credentials):
    with mock_iam():
        yield boto3.client('iam', region_name='ap-southeast-1')

@pytest.fixture(scope='module')
def sns_client(aws_credentials):
    with mock_sns():
        yield boto3.client('sns', region_name='ap-southeast-1')

@pytest.fixture(scope='module')
def ses_client(aws_credentials):
    with mock_ses():
        yield boto3.client('ses', region_name='ap-southeast-1')

@pytest.fixture(scope='module')
def lambda_context():
    lambda_context = {
        "function_name": "test",
        "memory_limit_in_mb": 128,
        "invoked_function_arn": "arn:aws:lambda:eu-west-1:809313241:function:test",
        "aws_request_id": "52fdfc07-2182-154f-163f-5f0f9a621d72",
    }

    return namedtuple("LambdaContext", lambda_context.keys())(*lambda_context.values())

@pytest.fixture(scope="module")
def test_data():
    #parent_dir = os.path.split(os.getcwd())[0]
    #filepath = parent_dir + '/tests/test_input_data.json'
    with open('test_functions_input_data.json') as json_data:
        test_data = json.load(json_data)
        return test_data
        
# Monkeypatch socket to prevent services from connecting to the internet if they try to do so
""" def guard(*args, **kwargs):
    raise Exception("Something tried to connect to the internet")
socket.socket = guard """