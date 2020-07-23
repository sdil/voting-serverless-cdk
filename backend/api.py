import logging
import os
import boto3
from aws_xray_sdk.core import xray_recorder, patch_all
from .models import Poll, Vote
from db.dynamodb import DynamoDBAdapter
import uuid 
from datetime import datetime
from collections import Counter

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

db = DynamoDBAdapter()

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


def create_poll(event, context):
    """
    Create a new voting poll
    """
    poll = Poll(uuid.uuid4(), datetime.now(), "test", {1: "1", 2: "2"}, Counter(), "user1")
    db.insert_poll(poll)


def update_vote(event, context):
    """
    Publish an message to SQS queue
    """
    pass
