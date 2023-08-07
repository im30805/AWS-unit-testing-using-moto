import importlib
from functionsForTestSetup.sqs_functions import sqs_client_setup

class TestSimpleSQS:
    def test_create_queue(self, sqs_client):
        with sqs_client_setup(sqs_client, "Example queue") as response:
            queue_url = response["QueueUrl"]
            assert "Example queue" in queue_url
            
            sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody="Testing mock SQS message"
            )
 
            message = sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
            ) 

            assert message["Messages"][0]["Body"] == "Testing mock SQS message"

            