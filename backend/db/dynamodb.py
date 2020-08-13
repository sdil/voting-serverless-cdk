from db.interface import AbstractDatabase
import boto3
import os
from typing import List
from models import Poll, Vote
from datetime import datetime


class DynamoDBAdapter(AbstractDatabase):
    def __init__(self):
        dynamodb = boto3.resource("dynamodb")
        self.poll_table = dynamodb.Table(os.environ.get("POLL_TABLE"))
        self.main_page_gsi = os.environ.get("MAIN_PAGE_GSI")

    def insert_poll(self, poll: Poll) -> None:
        self.poll_table.put_item(
            Item={
                "id": poll.id,
                "SK": "poll_info",
                "date": poll.date.isoformat(),
                "question": poll.question,
                "result": dict(poll.result),
                "SK1": poll.id,
                "PK1": poll.user,
                "PK2": poll.id,
            }
        )

    def get_poll(self, id: str) -> Poll:
        response = self.poll_table.get_item(Key={"id": id, "SK": "poll_info"})["Item"]

        return Poll(
            response["id"],
            datetime.fromisoformat(response["date"]),
            response["question"],
            response["result"],
            response.get("user"),
        )

    def get_all_polls(self) -> List[Poll]:
        response = self.poll_table.scan(IndexName=self.main_page_gsi)["Items"]
        polls = []

        for poll in response:
            poll = Poll(
                poll["id"],
                datetime.fromisoformat(poll["date"]),
                poll["question"],
                poll["result"],
            )
            polls.append(poll)

        return polls

    def update_poll(self, poll: Poll) -> None:
        """
        Update all answer result to the poll item
        """
        for (answer, count) in poll.result.items():
            # Iterate each of the answer to update them
            self.poll_table.update_item(
                Key={"id": poll.id, "SK": "poll_info"},
                UpdateExpression="SET #result.#answer = :count",
                ExpressionAttributeNames={"#result": "result", "#answer": answer},
                ExpressionAttributeValues={":count": count},
            )

    def insert_vote(self, vote: Vote) -> None:
        sk = f"{vote.id}#{vote.date.isoformat()}"
        self.poll_table.put_item(
            Item={
                "id": vote.poll,
                "SK": sk,
                "date": vote.date.isoformat(),
                "SK1": sk,
                "poll_id": vote.poll,
                "pk1": vote.user,
                "answer": vote.answer,
            }
        )
        return
