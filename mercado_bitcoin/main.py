import datetime
import time

from schedule import repeat, every, run_pending
from mercado_bitcoin.ingestors import AwsDaySummaryIngestor
from mercado_bitcoin.writers import S3Writter

if __name__ == "__main__":
    day_summary_ingestor = AwsDaySummaryIngestor(
        writer=S3Writter,
        coins=["BTC", "ETH", "LTC", "BCH"],
        default_start_date=datetime.date(2021, 6, 1),
    )

    @repeat(every(1).seconds)
    def job():
        day_summary_ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)
