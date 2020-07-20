import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def aggregate_vote_table(event, context):
    """
    Update aggregated-vote-db table with counts from vote-db table
    """
    logger.info("aggregate vote")
    logger.info(event)
    logger.info(context)
