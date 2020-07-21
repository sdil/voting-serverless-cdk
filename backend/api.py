import logging
import os
import boto3
from aws_xray_sdk.core import xray_recorder, patch_all


logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()


LUMIGO_TOKEN = os.environ.get("LUMIGO_TOKEN", "")


def get_all_votes(event, context):
    """
    Get most recent votes from aggregated-vote-db
    """
    logger.info("get all votes")


def get_vote_by_id(event, context):
    """
    Read a single vote item from aggregated-vote-db table
    """
    path = event.get("pathParameters").get("vote_id")
    logger.info(path)


def insert_new_vote(event, context):
    """
    Create a new voting poll
    """
    logger.info("test")


def update_vote(event, context):
    """
    Publish an message to SQS queue
    """
    pass
