from contextlib import contextmanager

# Use a context manager to help handle setup/teardown automatically before/after tests are run
@contextmanager
def sqs_resource_setup(sqs_resource, queue_name, attributes):
    queue = sqs_resource.create_queue(QueueName=queue_name, Attributes=attributes)
    yield queue

@contextmanager
def sqs_client_setup(sqs_client, queue_name):
    queue = sqs_client.create_queue(QueueName=queue_name)
    yield queue

# Queues
def ImportBulkProductQueue(sqs_client):
    queue_name = 'ImportBulkProductQueue'

    with sqs_client_setup(sqs_client, queue_name) as response:
        return response