import logging
import os

import boto3

logger = logging.getLogger(__name__)
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)  # Set logging level based on env variable LOGLEVEL. Defaults to Warning.


def lambda_handler(event, context):
    event_detail = event["detail"]  # As cloudwatch sends us some useless stuff we just want the detail
    error_code = event_detail.get("errorCode", None)

    # Does a quick check to make sure that the program was run against the correct exception. Even though the cloudwatch
    # event should do this. This is just in case.
    if error_code != "EntityAlreadyExistsException" or error_code is None:
        logging.error(f"Application ran against event that was not the correct exception please check the cloudwatch."
                      f"event. Error was {error_code}")
        raise SystemExit  # Exit

    account_id = event_detail["userIdentity"]["accountId"]
    mfa_device_name = event_detail["requestParameters"]["virtualMFADeviceName"]
    mfa_device_path = event_detail["requestParameters"]["path"]

    logger.info(f"MFA Device Information - Name {mfa_device_name}, path: {mfa_device_path}, accountId: {account_id}")

    mfa_device_arn = form_mfa_arn(account_id, mfa_device_name, mfa_device_path)  # Get the MFA device arn

    delete_mfa_device(mfa_device_arn)  # Delete it
    return


def form_mfa_arn(account_id: str, device_name: str, device_path: str) -> str:
    """Forms the MFA arn string

    Args:
        account_id (str): The account id where the MFA device lives
        device_name (str): The mfa devices name (Generally the username but can be different if using API/CLI)
        device_path (str): The mfa device path (Generally just / but can be different if using CLI/API)

    Returns:
        The full MFA arn for the device as a string
    """
    return f"arn:aws:iam::{account_id}:mfa{device_path}{device_name}"


def delete_mfa_device(mfa_arn: str):
    """Deletes the MFA device

    Args:
        mfa_arn (str): The virtual MFA devices arn
    """
    res = boto3.client("iam").delete_virtual_mfa_device(
        SerialNumber=mfa_arn
    )

    logger.debug(f"Delete Virtual MFA Device Response : {res}")

    return
