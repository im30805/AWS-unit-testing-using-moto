import os
import pytest
from botocore.exceptions import ClientError
import importlib  
from functionsForTestSetup.dynamodb_functions import SupplierMockTable, MerchantMockTable
from pathlib import Path

os.environ['SUPPLIER_TABLE'] = 'Supplier'
os.environ['MERCHANT_TABLE'] = 'Merchant'

class TestAdminDeleteSupplier:
    #################### Prepare the mock tables and data
    def test_change_to_current_path(self, base_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(base_path / "functions/ECOM-AdminDeleteSupplier" )
        
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
    def test_lambda_function(self, lambda_context):
        from lambda_function import lambda_handler
        
        example_event = {
            'arguments': {
                'supplierId': '000d6a93a-dd83-43b4-829d-c094918ef92d',
                'merchantId': '00c20727-ecdf-4799-b834-4b725f8e79df',
                'name': "Jojo's Bizzare Supplies",
                'address': "91, 123 Wryyy Street, Joestar Estate",
                'contact' : "0123456798",
                'email': "jjbs@example.com",
                'contactName': "Jojo",
                'country': "Singapore"
            }
        }

        response = lambda_handler(example_event, lambda_context)
        assert response['status'] == True
        assert response['message'] == 'Success to delete Supplier'
    
    def test_lambda_function_fail_delete_exception(self, lambda_context): # this test will fail
        from lambda_function import lambda_handler
        import uuid

        supplier_id = str(uuid.uuid4())

        example_event = {
            'arguments': {
                'supplierId': supplier_id,
                'merchantId': '00c20727-ecdf-4799-b834-4b725f8e79df',
                'name': "Jojo's Bizzare Supplies",
                'address': "91, 123 Wryyy Street, Joestar Estate",
                'contact' : "0123456798",
                'email': "jjbs@example.com",
                'contactName': "Jojo",
                'country': "Singapore"
            }
        }
         

        with pytest.raises(Exception):
            lambda_handler(example_event, lambda_context)  # should raise the exception 'Failed to delete Supplier'

    def test_lambda_function_empty_event(self, lambda_context):  # this test will fail, exception not raised, will return the standard error msg
        from lambda_function import lambda_handler
        example_event = {
            
        }

        with pytest.raises(Exception):
            lambda_handler(example_event, lambda_context)  # from the code, should raise the exception 'Invalid arguments'