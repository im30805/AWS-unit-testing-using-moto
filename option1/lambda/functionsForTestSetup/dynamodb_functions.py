from contextlib import contextmanager

# Use a context manager to help handle setup/teardown automatically before/after tests are run
@contextmanager
def dynamodb_setup(dynamodb_resource, table_name, key_schema, attribute_definition):

    dynamodb_resource.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definition,
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    yield

def dynamodb_create_gsi(dynamodb_client, table_name, attribute_definition, gsi_updates):
    try:
        dynamodb_client.update_table(
            TableName=table_name,
            # Any attributes used in the global secondary index must be declared in AttributeDefinitions
            AttributeDefinitions=attribute_definition,
            GlobalSecondaryIndexUpdates=gsi_updates    
        )
        return True

    except Exception as e:
        print("Error updating table:")
        print(e)

        return False

# Tables
def ProductMockTable(dynamodb_resource, dynamodb_client):
    with dynamodb_setup(
        dynamodb_resource, 
        table_name='Product', 
        key_schema=[{'AttributeName': 'productId','KeyType': 'HASH'}], 
        attribute_definition=[{'AttributeName': 'productId','AttributeType': 'S'}]
    ):

        dynamodb_create_gsi(dynamodb_client, 
        table_name='Product', 
        attribute_definition=[{"AttributeName": "merchantId","AttributeType": "S"},], 
        gsi_updates=[
            {
                "Create": {
                    "IndexName": "gsi-merchantId-title",
                    "KeySchema": [
                        {
                            "AttributeName": "merchantId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "title", 
                            "KeyType": "RANGE"
                        }

                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    }
                }
            }
        ]) 

        dynamodb_create_gsi(dynamodb_client, 
        table_name='Product', 
        attribute_definition=[{"AttributeName": "merchantId","AttributeType": "S"},], 
        gsi_updates=[
            {
                "Create": {
                    "IndexName": "gsi-merchantId-seoUrl",
                    "KeySchema": [
                        {
                            "AttributeName": "merchantId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "seoUrl", 
                            "KeyType": "RANGE"
                        }

                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    }
                }
            }]
        )

        return dynamodb_resource.Table('Product')

def ProductUOMMockTable(dynamodb_resource, dynamodb_client):
    with dynamodb_setup(
        dynamodb_resource, 
        table_name='ProductUOM', 
        key_schema=[{'AttributeName': 'productUOMId','KeyType': 'HASH'}], 
        attribute_definition=[{'AttributeName': 'productUOMId','AttributeType': 'S'}]
    ):

        dynamodb_create_gsi(dynamodb_client, 
        table_name='ProductUOM', 
        attribute_definition=[{"AttributeName": "merchantId","AttributeType": "S"},], 
        gsi_updates=[
            {
                "Create": {
                    "IndexName": "gsi-merchantId-productId",
                    "KeySchema": [
                        {
                            "AttributeName": "merchantId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "productId", 
                            "KeyType": "HASH"
                        }

                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    }
                }
            }
        ]) 

        dynamodb_create_gsi(dynamodb_client, 
        table_name='ProductUOM', 
        attribute_definition=[{"AttributeName": "merchantId","AttributeType": "S"},], 
        gsi_updates=[
            {
                "Create": {
                    "IndexName": "gsi-merchantId-sku",
                    "KeySchema": [
                        {
                            "AttributeName": "merchantId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "sku", 
                            "KeyType": "RANGE"
                        }

                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    }
                }
            }]
        )

        dynamodb_create_gsi(dynamodb_client, 
        table_name='ProductUOM', 
        attribute_definition=[{"AttributeName": "merchantId","AttributeType": "S"},], 
        gsi_updates=[
            {
                "Create": {
                    "IndexName": "gsi-merchantId-hotkey",
                    "KeySchema": [
                        {
                            "AttributeName": "merchantId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "hotkey", 
                            "KeyType": "RANGE"
                        }

                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    }
                }
            }]
        )

        return dynamodb_resource.Table('ProductUOM')

def StoreMockTable(dynamodb_resource, dynamodb_client):
    with dynamodb_setup(
        dynamodb_resource, 
        table_name='Store', 
        key_schema=[{'AttributeName': 'storeId','KeyType': 'HASH'}], 
        attribute_definition=[{'AttributeName': 'storeId','AttributeType': 'S'}]
    ):

        dynamodb_create_gsi(dynamodb_client, 
        table_name='Store', 
        attribute_definition=[{"AttributeName": "merchantId","AttributeType": "S"},], 
        gsi_updates=[
            {
                "Create": {
                    "IndexName": "gsi-merchantId-code",
                    "KeySchema": [
                        {
                            "AttributeName": "merchantId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "code", 
                            "KeyType": "RANGE"
                        }

                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    }
                }
            }
        ]) 

        dynamodb_create_gsi(dynamodb_client, 
        table_name='Store', 
        attribute_definition=[{"AttributeName": "merchantId","AttributeType": "S"},], 
        gsi_updates=[
            {
                "Create": {
                    "IndexName": "gsi-merchantId-priceGroupName",
                    "KeySchema": [
                        {
                            "AttributeName": "merchantId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "priceGroupName", 
                            "KeyType": "RANGE"
                        }

                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    }
                }
            }]
        )

        dynamodb_create_gsi(dynamodb_client, 
        table_name='Store', 
        attribute_definition=[{"AttributeName": "merchantId","AttributeType": "S"},], 
        gsi_updates=[
            {
                "Create": {
                    "IndexName": "gsi-merchantId-salesChannelName",
                    "KeySchema": [
                        {
                            "AttributeName": "merchantId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "salesChannelName", 
                            "KeyType": "RANGE"
                        }

                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    }
                }
            }]
        )

        return dynamodb_resource.Table('Store')

def MerchantMockTable(dynamodb_resource):
    with dynamodb_setup(
        dynamodb_resource, 
        table_name='Merchant', 
        key_schema=[{'AttributeName': 'merchantId','KeyType': 'HASH'}], 
        attribute_definition=[{'AttributeName': 'merchantId','AttributeType': 'S'}]
    ):

        initial_item = {
            'merchantId': '00c20727-ecdf-4799-b834-4b725f8e4322',
            'address': '12, Jalan Padang 4/5',
            'createdAt': '2021-06-30T18:03:59.323321Z',
            'currency': 'MYR',
            'domain': 'www.example.com',
            'merchantName': 'Hello Store',
            'name': 'Hello',
            'notificationEmail': 'example@email.com'
        }
        
        table = dynamodb_resource.Table('Merchant')
        table.put_item(Item=initial_item)

        return table

def SupplierMockTable(dynamodb_resource, dynamodb_client):
    with dynamodb_setup(
        dynamodb_resource, 
        table_name='Supplier', 
        key_schema=[{'AttributeName': 'supplierId','KeyType': 'HASH'}], 
        attribute_definition=[{'AttributeName': 'supplierId','AttributeType': 'S'}]
    ):
        dynamodb_create_gsi(dynamodb_client, 
        table_name='Supplier', 
        attribute_definition=[{"AttributeName": "merchantId","AttributeType": "S"},], 
        gsi_updates=[
            {
                "Create": {
                    "IndexName": "gsi-merchantId-name",
                    "KeySchema": [
                        {
                            "AttributeName": "merchantId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "name", 
                            "KeyType": "RANGE"
                        }

                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    }
                }
            }
        ]) 

        initial_item = {
            'supplierId': '000d6a93a-dd83-43b4-829d-2394918ef92d',
            'merchantId': '00c20727-ecdf-4799-b834-43333f8e79df',
            'name': "Jojo's Bizzare Supplies",
            'address': "12, Jalan Contoh 3/4, 56789 Petaling Jaya, Selangor",
            'contact' : "0123456798",
            'email': "jjbs@example.com",
            'contactName': "Jojo",
            'country': "Malaysia"
        }
        
        table = dynamodb_resource.Table('Supplier')
        table.put_item(Item=initial_item)
        
        return table
