"""
"""
import json
import os
from pathlib import Path

import boto3
from botocore.config import Config

INSTANCE_NAME = "valheim-01"

SECRETS_FILE = os.getenv("DOUGS_AWS_SECRETS", None)
if SECRETS_FILE is None:
    SECRETS_FILE = Path("secrets.json")


BOTOCONFIG = Config(
    region_name="us-west-2",
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)


def read_secrets(secrets_file=SECRETS_FILE):
    with open(secrets_file, "r") as openf:
        data = json.load(openf)

    return data


def get_status():
    """
    Get the status of the EC2 instance.
    """

    secrets = read_secrets()

    ec2 = boto3.client(
        "ec2",
        aws_access_key_id=secrets["aws_access_key"],
        aws_secret_access_key=secrets["aws_secret_access_key"],
        config=BOTOCONFIG,
    )

    filter = [{"Name": "tag:Name", "Values": [INSTANCE_NAME]}]

    response = ec2.describe_instances(Filters=filter)

    print(response)
