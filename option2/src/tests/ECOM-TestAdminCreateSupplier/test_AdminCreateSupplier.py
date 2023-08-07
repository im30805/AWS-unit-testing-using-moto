import os
import pytest
from botocore.exceptions import ClientError
import importlib  
from boto3.dynamodb.conditions import Key
from functionsForTestSetup.dynamodb_functions import *

os.environ['SUPPLIER_TABLE'] = 'Supplier'
os.environ['MERCHANT_TABLE'] = 'Merchant'

@pytest.fixture(scope="function")
def test_inputs(test_data):
    return test_data['tests']['test_AdminCreateSupplier']
    
#@pytest.mark.incremental
class TestAdminCreateSupplier:
    #################### Prepare the mock tables and data
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
    def test_check_supplier_return_exception(self):
        lambda_function = importlib.import_module("lambda.functions.ECOM-AdminCreateSupplier.lambda_function")

        merchantId = '00c20727-ecdf-4799-b834-4b725f8e79df'
        name = "Jojo's Bizzare Supplies"

        with pytest.raises(Exception) as e_info:
            lambda_function.checkSupplierName(merchantId, name)
    
    def test_create_supplier(self, dynamodb_resource, test_inputs):
        lambda_function = importlib.import_module("lambda.functions.ECOM-AdminCreateSupplier.lambda_function")
        
        # merchantId = '00c20727-ecdf-4799-b834-4b725f8e79df'
        # name = "Example Supplier"
        # address = "234/22 Test Street"
        # contact = "0198766543"
        # email = "eg@egmail.com"
        # contactName = "Mr Twister"
        # country = "Malaysia"
        
        arguments = test_inputs['test_create_supplier']
        merchantId = arguments['merchantId']
        name = arguments['name']
        address = arguments['address']
        contact = arguments['contact']
        email = arguments['email']
        contactName = arguments['contactName']
        country = arguments['country']
        
        supplier = lambda_function.createSupplier(merchantId, name, address, contact, email, contactName, country)

        assert supplier['name'] == "Example Supplier"

        table = dynamodb_resource.Table('Supplier')

        response = table.query(
            IndexName='gsi-merchantId-name',
            KeyConditionExpression=Key('merchantId').eq(merchantId) & Key('name').eq(name)
        )

        assert response['Items'][0]['name'] == "Example Supplier"
    
    @pytest.mark.parametrize(
    "test_input, expected_response",
    [
        pytest.param({}, "Invalid Arguments.", id="empty_event"),
        pytest.param(
            {
                'arguments': {
                    'merchantId': '00c20727-ecdf-4799-b834-4b725f8e79df',
                    'name': "Jojo's Bizzare Supplies",
                    'address': "12, Jalan Contoh 3/4, 56789 Petaling Jaya, Selangor",
                    'contact' : "0123456798",
                    'email': "jjbs@example.com",
                    'contactName': "Jojo",
                    'country': "Malaysia"
                }
            }, 
            "The server encountered an unexpected condition that prevented it from fulfilling your request.", 
            id="supplier_already_exist"
        ),
    ],
    )
    def test_lambda_function_test_invalid_parametrize(self, test_input, expected_response, lambda_context):
        lambda_function = importlib.import_module("lambda.functions.ECOM-AdminCreateSupplier.lambda_function")

        response = lambda_function.lambda_handler(test_input, lambda_context)
        assert response.get('message') == expected_response
    
    def test_lambda_function_valid(self, lambda_context):      
        lambda_function = importlib.import_module("lambda.functions.ECOM-AdminCreateSupplier.lambda_function")
  
        example_event = {
            'arguments': {
                'merchantId': '00c20727-ecdf-4799-b834-4b725f8e79df',
                'name': "Supplies Inc.",
                'address': "45, Jalan Contoh 5/6, 56789 Petaling Jaya, Selangor",
                'contact' : "0129876543",
                'email': "sup@example.com",
                'contactName': "Cool",
                'country': "Malaysia"
            }
        }

        response = lambda_function.lambda_handler(example_event, lambda_context)
        assert isinstance(response.get('supplierId'), str)
        assert response.get('status') == True
        assert response.get('message') == 'Supplier created successfully.'
