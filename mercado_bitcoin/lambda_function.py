import datetime

from mercado_bitcoin.ingestors import AwsDaySummaryIngestor
from mercado_bitcoin.writers import S3Writter
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    logger.info(f"{event}")
    logger.info(f"{context}")

    AwsDaySummaryIngestor(
        writer=S3Writter,
        coins=["BTC", "ETH", "LTC", "BCH"],
        default_start_date=datetime.date(2021, 6, 1),
    ).ingest()
