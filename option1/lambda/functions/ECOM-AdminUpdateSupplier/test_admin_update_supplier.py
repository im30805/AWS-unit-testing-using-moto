import os
import pytest
from botocore.exceptions import ClientError
import importlib  
from functionsForTestSetup.dynamodb_functions import SupplierMockTable, MerchantMockTable
from pathlib import Path

os.environ['SUPPLIER_TABLE'] = 'Supplier'
os.environ['MERCHANT_TABLE'] = 'Merchant'

@pytest.fixture(scope="function")
def test_inputs(test_data):
    return test_data['tests']['test_AdminUpdateSupplier']

class TestAdminUpdateSupplier:
    #################### Prepare the mock tables and data
    # an attempt to change to current test directory if pytest needs to run multiple tests from another part of the directory
    # due to each directory having the same filename of lambda_function.py, side effects happen
    def test_change_to_current_path(self, base_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(base_path / "functions/ECOM-AdminUpdateSupplier" )
        
    def test_create_ddb_tables(self, dynamodb_resource, dynamodb_client):
        SupplierTable = SupplierMockTable(dynamodb_resource, dynamodb_client)
        assert SupplierTable.name == 'Supplier'
        assert SupplierTable.global_secondary_indexes[0]['IndexName'] == "gsi-merchantId-name"

        MerchantTable = MerchantMockTable(dynamodb_resource)
        assert MerchantTable.name == 'Merchant'
    
    """ def test_list_tables(self, capsys):
        import boto3
        listing = boto3.client('dynamodb', region_name='us-east-1').list_tables()
        print(listing)
        captured = capsys.readouterr()
        assert captured.out == listing """
    
    def test_get_initial_supplier(self, dynamodb_resource):
        table = dynamodb_resource.Table('Supplier')

        response = table.get_item(
            Key={
                'supplierId': '000d6a93a-dd83-43b4-829d-c094918ef92d'
            }
        )

        assert response['Item']['supplierId'] == '000d6a93a-dd83-43b4-829d-c094918ef92d'
        assert response['Item']['name'] == "Jojo's Bizzare Supplies"
    
    def test_get_initial_merchant(self, dynamodb_resource):
        table = dynamodb_resource.Table('Merchant')

        response = table.get_item(
            Key={
                'merchantId': '00c20727-ecdf-4799-b834-4b725f8e79df'
            }
        )

        assert response['Item']['merchantId'] == '00c20727-ecdf-4799-b834-4b725f8e79df'
        assert response['Item']['name'] == 'Jeff Merchant'
    
    #################### Lambda function test cases 
    def test_lambda_function_missing_arguments(self, test_inputs, lambda_context):  # pass in the test_inputs fixture
        lambda_function = importlib.import_module("lambda.functions.ECOM-AdminUpdateSupplier.lambda_function")

        example_event = test_inputs['test_lambda_function_missing_arguments']

        response = lambda_function.lambda_handler(example_event, lambda_context)
        assert response['status'] == False
        assert response['message'] == "The server encountered an unexpected condition that prevented it from fulfilling your request."

    def test_lambda_function(self, test_inputs, lambda_context):
        lambda_function = importlib.import_module("lambda.functions.ECOM-AdminUpdateSupplier.lambda_function")

        example_event = test_inputs['test_lambda_function']

        response = lambda_function.lambda_handler(example_event, lambda_context)
        assert response['status'] == True
        assert response['message'] == 'Supplier Updated.'
        