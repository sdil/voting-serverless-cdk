import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_votes():
    """
    Get most recent votes from aggregated-vote-db
    """
    pass


def get_vote_by_id():
    """
    Read a single vote item from aggregated-vote-db table
    """
    pass


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
