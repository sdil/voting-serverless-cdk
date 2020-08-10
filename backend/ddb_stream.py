# Reference: https://github.com/linuxacademy/content-dynamodb-deepdive/blob/master/6.2.2-Aggregation_With_Streams/lambda_function.py

import decimal

import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from models import Poll
from db.dynamodb import DynamoDBAdapter

poll_table = dynamodb.Table(os.environ.get("POLL_TABLE"))
table = boto3.resource("dynamodb").Table(poll_table)
td = TypeDeserializer()
db = DynamoDBAdapter()


def lambda_handler(event, context):
    # Use in application cache so that it refresh everytime it runs
    polls = []

    for record in event["Records"]:
        data = record["dynamodb"].get("NewImage")
        d = {}
        for key in data:
            d[key] = td.deserialize(data[key])

        try:
            # Check if the poll is already in the application cache
            # If it's not in cache, fetch from DynamoDB
            polls[d["poll_id"]]
        except KeyError:
            polls[d["poll_id"]] = db.get_poll(d["poll_id"])

        polls[d["id"]].result = process_poll_result()

    for poll in polls:
        update_vote_result(poll)

    print("Successfully processed {} records.".format(len(event["Records"])))


def process_poll_result():

    existing_result = polls[d["poll_id"]].result
    return existing_result[int(d["vote_choice"])] + 1


def update_vote_result(poll):
    try:
        print(f"Updating aggregate votes for {poll.id}. Poll result: {poll.result}}")

        table.update_item(
            Key={"segment": candidate},
            UpdateExpression="SET votes = votes + :val",
            ExpressionAttributeValues={":val": decimal.Decimal(sum)},
        )
    except ClientError as e:
        print(f'{e.response["Error"]["Code"]}: {e.response["Error"]["Message"]}')
        raise
    else:
        print("Aggregate votes updated")
