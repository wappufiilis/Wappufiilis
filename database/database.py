import os
import random
from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")


def putItem(year, guild, score):
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE_NAME"))
    timestamp = int(datetime.now().timestamp())
    rand = random.randint(0, 100000)
    table.put_item(
        Item={
            "partition_key": f"{year}::{guild}::{rand}",
            "year": year,
            "guild": guild,
            "score": score,
            "timestamp": timestamp,
        }
    )
