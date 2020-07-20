import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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


def update_vote():
    """
    Publish an message to SQS queue
    """
    pass
