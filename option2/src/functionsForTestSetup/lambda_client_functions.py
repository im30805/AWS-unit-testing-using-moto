from contextlib import contextmanager
import io
import zipfile
from iam_role_functions import create_iam_role

def create_zip(filename, pfunc):
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED)
    zip_file.writestr(filename, pfunc)
    zip_file.close()
    zip_output.seek(0)
    return zip_output.read()

@contextmanager
def create_mock_lambda(lambda_client, lambda_name, code, iam_role):
    lambda_client.create_function(
        FunctionName=lambda_name,
        Runtime='python3.7',
        Role=iam_role,
        Handler='lambda_function.lambda_handler',
        Code={
            'ZipFile': code,
        },
        Description='Test invoke function for ' + lambda_name,
        Timeout=3,
        MemorySize=128,
        Publish=True
    )

    yield

def create_mock_AdminCreateProduct(lambda_client):
    pfunc = '''
            Code should go here, I think
            I couldn't figure out in time
            I don't know if I was doing it correctly or not
            '''
    code = create_zip("AdminCreateProduct.py", pfunc)
    create_mock_lambda(lambda_client, "ECOM-AdminCreateProduct", code)