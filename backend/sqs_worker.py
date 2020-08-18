# Reference: https://github.com/linuxacademy/content-dynamodb-deepdive/blob/master/6.3.3-SQS-Write-Buffer/lambda_function.py
# Reference: https://docs.aws.amazon.com/lambda/latest/dg/with-sqs-create-package.html#with-sqs-example-deployment-pkg-python

import boto3
from datetime import datetime
import uuid
import logging
from models import Vote
import os
from db.dynamodb import DynamoDBAdapter
import json


DYNAMODB_TABLE = os.environ["POLL_TABLE"]
db = DynamoDBAdapter()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def insert_to_vote_db_table(event, context):
    """
    Example message from Lambda HTTP API:
    {
        "poll": 1
        "answer": "cat"
        "date": "2020-07-23 04:19:26.819419"
    }
    """

    for message in event["Records"]:

        logger.info(message)
        body = json.loads(message["body"])
        vote = Vote(
            id=f"vote_{uuid.uuid4()}",
            date=datetime.fromisoformat(body["date"]),
            poll=body["poll"],
            answer=body["answer"],
        )

        response = db.insert_vote(vote)
        logger.info(f"inserted vote {vote.id} to dynamodb")
