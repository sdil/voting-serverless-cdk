from db.interface import AbstractDatabase
import boto3
import os
from models import Poll
from datetime import datetime


class DynamoDBAdapter(AbstractDatabase):
    def __init__(self):
        dynamodb = boto3.resource("dynamodb")
        self.poll_table = dynamodb.Table(os.environ.get("POLL_TABLE"))

    def insert_poll(self, poll: Poll):
        self.poll_table.put_item(
            Item={
                "id": poll.id,
                "SK": "poll_info",
                "date": poll.date.isoformat(),
                "question": poll.question,
                "result": dict(poll.result),
                "user": poll.user,
                "SK1": poll.id,
                "PK1": poll.user,
                "PK2": poll.id,
            }
        )

    def get_poll(self, id: str):
        response = self.poll_table.get_item(Key={"id": id, "SK": "poll_info"})["Item"]

        return Poll(
            response["id"],
            datetime.fromisoformat(response["date"]),
            response["question"],
            response["result"],
            response["user"],
        )
