# -*- coding: utf-8 -*-
"""
"""
import json
import os
import time
from pathlib import Path
from typing import Dict
from typing import Optional
from typing import Union

import boto3
from botocore.config import Config

from . import logger

# TODO: It would be prudent to make the instance ID dynamic so that I can
# rebuild the instance when needed.
INSTANCE_ID = "i-09be78544d62ec3c2"

SECRETS_FILE: Union[str, Path] = os.getenv("DOUGS_AWS_SECRETS", Path("secrets.json"))

BOTOCONFIG = Config(
    region_name="us-west-2",
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)


def read_secrets(secrets_file: Union[str, Path] = SECRETS_FILE) -> Dict[str, str]:
    logger.debug(f"Reading secrets file '{secrets_file}'")
    with open(secrets_file, "r") as openf:
        data = json.load(openf)

    return data


def _get_resource() -> boto3.resource:
    """
    Create the Boto3 EC2 resource object.
    """
    secrets = read_secrets()
    ec2 = boto3.resource(
        "ec2",
        aws_access_key_id=secrets["aws_access_key"],
        aws_secret_access_key=secrets["aws_secret_access_key"],
        config=BOTOCONFIG,
    )
    return ec2


def _get_instance():
    """
    Create the Boto3 EC2 Instance object.
    """
    ec2 = _get_resource()
    instance = ec2.Instance(INSTANCE_ID)
    return instance


def allocate_and_associate_elastic_ip(instance) -> Dict[str, str]:
    logger.debug("Allocating and associating IP address.")
    instance.reload()
    ec2 = instance.meta.client
    allocation = ec2.allocate_address(Domain="vpc")
    ec2.associate_address(
        AllocationId=allocation["AllocationId"], InstanceId=INSTANCE_ID
    )
    return allocation


def disassociate_and_release_elastic_ip(instance) -> None:
    logger.debug("Disassociating and releasing IP address.")
    # I have no idea why, but I need to explicitly set PublicIp="" or else
    # we get:
    #   An error occurred (InvalidParameterCombination) when calling the
    #   ReleaseAddress operation: You may specify public IP or allocation id,
    #   but not both in the same call
    instance.reload()
    addr = instance.classic_address
    if addr is None:
        logger.warning("Instance does not have an associated elastic IP.")
        return

    logger.debug(f"IP: {addr}")
    addr.disassociate()
    addr.release(AllocationId=addr.allocation_id, PublicIp="")


def get_ip(instance) -> str:
    """
    Get the public IP of the EC2 instance.
    """
    instance.reload()
    ip = instance.public_ip_address
    logger.debug(f"Got ip: {ip}")
    return ip


def get_status(instance) -> str:
    """
    Get the status of the EC2 instance.
    """
    # AWS puts tags in as a list of dicts, where the dict keys are "Key" and "Value"
    # This searches through all the AWS tags searching for the "Name" key.
    instance_name = [t["Value"] for t in instance.tags if t["Key"] == "Name"][0]
    logger.debug(f"Getting status of instance: {instance_name}")

    instance.reload()
    status = instance.state["Name"].lower()
    logger.debug(f"Status: {status}")
    return status


def print_status(status: str, ip: Optional[str] = None) -> None:
    """
    Print the status of the EC2 instance.
    """
    status = status.upper()
    status_text = {
        "STOPPED": (
            f"The server is {status}. Run `dougs_valheim_server start` to start it."
        ),
        "RUNNING": f"The server is {status} with an IP address of: {ip}.",
        "PENDING": f"The server is {status}. Please check back later.",
        "STOPPING": f"The server is {status}. Please check back later.",
    }

    try:
        print(status_text[status])
    except KeyError:
        raise ValueError(f"Unknown server state '{status}'. Please check later.")


def start_instance(instance) -> None:
    logger.debug("Starting instance.")
    # First check to see if we actually need to act.
    status = get_status(instance)
    if status == "running":
        print("Instance is already running.")
        return
    elif status in ("pending", "stopping"):
        print(f"Server is in the transition state '{status}'. Please try again later.")
        return

    print("Starting server...")
    instance.start()

    # Simple polling to check when the server comes up.
    for _ in range(45):
        status = get_status(instance)
        if status == "running":
            break
        time.sleep(1)
    else:
        print("Server failed to start in the allotted time. Please check later.")
        return

    # Whenever we tear down the server, we delete the elastic IP so that we
    # don't get charged for unused ones. Thus we have to allocate and assign.
    allocate_and_associate_elastic_ip(instance)
    ip = get_ip(instance)

    print(f"The server has been started. IP address: {ip}")


def stop_instance(instance) -> None:
    logger.debug("Stopping instance.")
    status = get_status(instance)
    if status == "stopped":
        print("Instance is already stopped.")
        return
    elif status in ("pending", "stopping"):
        print(f"Server is in the transition state '{status}'. Please try again later.")
        return

    print("Stopping server...")
    instance.stop()

    # Don't want to get charged for unused IPs!
    disassociate_and_release_elastic_ip(instance)

    print("Stopped")
