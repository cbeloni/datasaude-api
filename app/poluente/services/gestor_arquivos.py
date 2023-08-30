import boto3, os
from dotenv import load_dotenv
from io import BytesIO
from distutils import log
load_dotenv()

aws_access_key_id = os.environ.get('aws_access_key_id')
aws_secret_access_key = os.environ.get('aws_secret_access_key')
endpoint_url = os.environ.get('endpoint_url')
log.info("loading configs")
log.info(aws_access_key_id)
log.info(aws_secret_access_key)
log.info(endpoint_url)

_s3_client = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          endpoint_url=endpoint_url)


def enviar_arquivo(bucket_name: str, file: bytes, object_name: str, content_type: str, ):
    extra_args = {'ContentType': content_type}
    _s3_client.upload_fileobj(BytesIO(file), bucket_name, object_name, ExtraArgs=extra_args)

def listar_arquivo(bucket_name: str):
    response = _s3_client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print('O bucket está vazio.')


def remover_arquivo(bucket_name: str, key: str):
    bucket_name = bucket_name
    object_key = key

    return _s3_client.delete_object(Bucket=bucket_name, Key=object_key)