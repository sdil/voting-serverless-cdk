import logging
import os
from lumigo_tracer import lumigo_tracer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LUMIGO_TOKEN = os.environ.get("LUMIGO_TOKEN", "")


@lumigo_tracer(token=LUMIGO_TOKEN, enhance_print=True)
def get_all_votes(event, context):
    """
    Get most recent votes from aggregated-vote-db
    """
    logger.info("get all votes")


@lumigo_tracer(token=LUMIGO_TOKEN, enhance_print=True)
def get_vote_by_id(event, context):
    """
    Read a single vote item from aggregated-vote-db table
    """
    path = event.get("pathParameters").get("vote_id")
    logger.info(path)


@lumigo_tracer(token=LUMIGO_TOKEN, enhance_print=True)
def insert_new_vote(event, context):
    """
    Create a new voting poll
    """
    logger.info("test")


@lumigo_tracer(token=LUMIGO_TOKEN, enhance_print=True)
def update_vote():
    """
    Publish an message to SQS queue
    """
    pass
