import dataclasses
import json
import logging
import os
import uuid
from collections import Counter
from datetime import datetime

import boto3
from aws_xray_sdk.core import patch_all, xray_recorder
from botocore.exceptions import ClientError


from db.dynamodb import DynamoDBAdapter
from models import Poll, Vote


logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()
sqs = boto3.client("sqs")


db = DynamoDBAdapter()
queue_url = os.environ.get("VOTING_QUEUE_URL")


def get_all_votes(event, context):
    """
    Get most recent polls from ddb
    """

    logger.info("get all polls")
    polls = db.get_all_polls()
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": Poll.schema().dumps(polls, many=True),
    }


def get_vote_by_id(event, context):
    """
    Read a single vote item from ddb
    """
    id = event.get("pathParameters").get("vote_id")
    poll = db.get_poll(id)

    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": poll.to_json(),
    }


def create_poll(event, context):
    """
    Create a new voting poll
    """
    poll = Poll(
        uuid.uuid4(),
        datetime.now(),
        "what if cat rule the world?",
        Counter({"poops everywhere": 0, "king of love": 0}),
        "user1",
    )
    db.insert_poll(poll)

    msg = {
        "status": "success",
        "headers": {"content-type": "application/json"},
        "message": f"poll {poll.id} is created",
    }

    return {"statusCode": 200, "body": json.dumps(msg)}


def vote(event, context):
    """
    Publish an message to SQS queue.

    Example message from frontend:
    {
        "poll": "uuid1"
        "answer": "cat"
    }
    """
    logger.info(event)
    event["date"] = datetime.now().isoformat()

    msg = json.dumps(event)

    try:
        response = sqs.send_message(
            QueueUrl="https://sqs.us-east-2.amazonaws.com/836476550359/voting-serverless-cdk-votingqueueD7A5A12E-1FC6Y6V1ASS3H",
            MessageBody=msg,
        )
        logging.info("MessageId: " + response["MessageId"])
    except ClientError as e:
        print(f'{e.response["Error"]["Code"]}: {e.response["Error"]["Message"]}')
    else:
        print(response)
