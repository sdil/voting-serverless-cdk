# Reference: https://github.com/linuxacademy/content-dynamodb-deepdive/blob/master/6.3.3-SQS-Write-Buffer/lambda_function.py

import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import uuid
import os
from db.dynamodb import DynamoDBAdapter


QUEUE_NAME = os.environ["VOTING_QUEUE"]
DYNAMODB_TABLE = os.environ["POLL_TABLE"]

sqs = boto3.resource("sqs")

db = DynamoDBAdapter()


def insert_to_vote_db_table(event, context):
    """
    Example message from Lambda HTTP API:
    {
        "poll": 1
        "answer": "cat"
        "date": "2020-07-23 04:19:26.819419"
    }
    """
    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)

    while True:
        for message in queue.receive_messages(MaxNumberOfMessages=10):
            print(message)

            vote = Vote(
                id=uuid.uuid4(),
                date=datetime.fromisoformat(message["date"]),
                poll=message["poll"],
                answer=message["answer"],
            )

            try:
                response = db.insert_vote(vote)
                print("Wrote message to DynamoDB:", json.dumps(response))
                message.delete()
                print("Deleted a processed message:", message.message_id)
            except ClientError as e:
                print(
                    f'{e.response["Error"]["Code"]}: {e.response["Error"]["Message"]}'
                )
            else:
                print(response)
