import pytest
from botocore.exceptions import ClientError
import os
import importlib
from functionsForTestSetup.dynamodb_functions import GalleryDetailMockTable, ImportJobMockTable, ProductMockTable, ProductUOMMockTable, StoreMockTable
from functionsForTestSetup.s3_functions import EcomBulkUploadBucketDev, list_buckets

os.environ['GALLERY_DETAIL_TABLE'] = 'GalleryDetail'
os.environ['IMPORT_JOB_TABLE'] = 'ImportJob'
os.environ['PRODUCT_TABLE'] = 'Product'
os.environ['PRODUCT_UOM_TABLE'] = 'ProductUOM'
os.environ['STORE_TABLE'] =	'Store'
os.environ['WEBASSETS_BUCKET']	= 'ecom-webassets-dev'
os.environ['BULK_UPLOAD_BUCKET'] = 'ecom-bulk-upload-bucket-dev'
os.environ['ADMIN_CREATE_PRODUCT_LAMBDA'] = 'ECOM-AdminCreateProduct'

class TestInsertBulkProductFromSQS:
    
    def test_create_ddb_tables(self, dynamodb_resource, dynamodb_client):
        GalleryDetailTable = GalleryDetailMockTable(dynamodb_resource, dynamodb_client)
        assert GalleryDetailTable.name == 'GalleryDetail'
        assert GalleryDetailTable.global_secondary_indexes[0]['IndexName'] == 'gsi-merchantId-name'

        ImportJobTable = ImportJobMockTable(dynamodb_resource)
        assert ImportJobTable.name == 'ImportJob'

        ProductTable = ProductMockTable(dynamodb_resource, dynamodb_client)
        assert ProductTable.name == 'Product'
        assert ProductTable.global_secondary_indexes[0]['IndexName'] == 'gsi-merchantId-title'

        ProductUOMTable = ProductUOMMockTable(dynamodb_resource, dynamodb_client)
        assert ProductUOMTable.name == 'ProductUOM'
        assert ProductUOMTable.global_secondary_indexes[0]['IndexName'] == "gsi-merchantId-productId"
        assert ProductUOMTable.global_secondary_indexes[1]['IndexName'] == "gsi-merchantId-sku"
        assert ProductUOMTable.global_secondary_indexes[2]['IndexName'] == "gsi-merchantId-hotkey"

        StoreTable = StoreMockTable(dynamodb_resource, dynamodb_client)
        assert StoreTable.name == 'Store'
        assert StoreTable.global_secondary_indexes[0]['IndexName'] == "gsi-merchantId-code"
        assert StoreTable.global_secondary_indexes[1]['IndexName'] == "gsi-merchantId-priceGroupName"
        assert StoreTable.global_secondary_indexes[2]['IndexName'] == "gsi-merchantId-salesChannelName"
    
    def test_create_s3_buckets(self, s3_client):
        assert EcomBulkUploadBucketDev(s3_client) == True

        assert list_buckets(s3_client) == ['ecom-bulk-upload-bucket-dev']
    
    def test_lambda_handler(self, lambda_context):
        lambda_function = importlib.import_module("lambda.functions.ECOM-InsertBulkProductFromSQS.lambda_function")
        test_event = {
            "Records": [ 
                {
                    "body": {
                        "merchantId": "",
                        "importJobId": "",
                        "s3_path": "",
                        "bucketName": "",
                        "identity": "",
                        "key": "",
                    }

                }
            ]}

