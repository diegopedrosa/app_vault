import boto3
import os
from base64 import b64decode, b64encode

def encrypt(value):
    return b64encode(
        boto3.client('kms').encrypt(KeyId=os.environ['keyid'],
                                    Plaintext=value)['CiphertextBlob'])


def decrypt(value):
    d = boto3.client('kms').decrypt(CiphertextBlob=b64decode(value))
    return (d['Plaintext'].decode('utf-8'))
    