import datetime
import json
import os
from tempfile import NamedTemporaryFile
from typing import List

import boto3


class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)


class DataWriter:
    def __init__(self, coin: str, api: str) -> None:
        self.api = api
        self.coin = coin
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now()}.json"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as f:
            f.write(row)

    def _write_to_file(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)

    def write(self, data: [List, dict]):
        self._write_to_file(data=data)


class S3Writter(DataWriter):
    def __init__(self, coin: str, api: str):
        super().__init__(coin, api)
        self.tempfile = NamedTemporaryFile()
        self.client = boto3.client("s3")
        self.key = f"mercado_bitcoin/{self.api}/coin={self.coin}/extracted_at={datetime.datetime.now().date()}/{self.api}_{self.coin}_{datetime.datetime.now()}.json"

    def _write_row(self, row: str) -> None:
        with open(self.tempfile.name, "a") as f:
            f.write(row)

    def write(self, data: [List, dict]):
        self._write_to_file(data=data)
        self._write_file_to_s3()

    def _write_file_to_s3(self):
        self.client.put_object(
            Body=self.tempfile, Bucket="belisco-data-lake-raw", Key=self.key
        )
