# Reference: https://github.com/linuxacademy/content-dynamodb-deepdive/blob/master/6.2.2-Aggregation_With_Streams/lambda_function.py

import decimal

import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from models import Poll
from db.dynamodb import DynamoDBAdapter
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

td = TypeDeserializer()
db = DynamoDBAdapter()


def aggregate_vote_table(event, context):
    logger.info(event)

    # Use in application cache so that it refresh everytime it runs
    polls = {}

    for record in event["Records"]:
        logger.info(record)

        if record["eventName"] != "INSERT":
            # If it's other operation other than INSERT, ignore it
            continue

        data = record["dynamodb"].get("NewImage")
        d = {}
        for key in data:
            d[key] = td.deserialize(data[key])

        if not d["SK"].startswith("vote_"):
            # If the new data is not vote data, skip it
            continue

        try:
            # Check if the poll is already in the application cache
            # If it's not in cache, fetch from DynamoDB
            polls[d["poll_id"]]

        except KeyError:
            polls[d["poll_id"]] = db.get_poll(d["poll_id"])

        # Increase the result count
        polls[d["id"]].result[d["answer"]] += 1

    for poll in polls.values():
        update_vote_result(poll)

    logger.info("Successfully processed {} records.".format(len(event["Records"])))


def update_vote_result(poll):
    logger.info(type(poll))
    try:
        logger.info(f"Persisting vote result for {poll}")
        db.update_poll(poll)
    except ClientError as e:
        logger.info(f'{e.response["Error"]["Code"]}: {e.response["Error"]["Message"]}')
        raise
    else:
        logger.info("Aggregate votes updated")
