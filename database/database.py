import os
import random
from datetime import datetime

import boto3
from botocore.credentials import Credentials

creds = Credentials(
    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
client = boto3.client(
    "dynamodb",
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=creds.access_key,
    aws_secret_access_key=creds.secret_key,
)
dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_DEFAULT_REGION"))


def saveUserInfo(
    user_id: str,
    campus: str = None,
    guild: str = None,
    year: str = None,
    lastWappuFiilis: int = None,
    lastWappuFiilisTimestamp: int = None,
):
    """
    Save user info, if user already exists, update the info
    """
    table = dynamodb.Table(os.getenv("DYNAMODB_USERS_TABLE_NAME"))
    table.put_item(
        Item={
            "partition_key": f"user::{user_id}",
            "user_id": user_id,
            "campus": campus,
            "guild": guild,
            "year": year,
            "lastWappuFiilis": lastWappuFiilis,
            "lastWappuFiilisTimestamp": lastWappuFiilisTimestamp,
        }
    )


def getUserInfo(user_id: str) -> dict:
    """
    Get user info
    If no user exists, return None
    """
    print("aws", os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY"))
    table = dynamodb.Table(os.getenv("DYNAMODB_USERS_TABLE_NAME"))
    response = table.get_item(Key={"partition_key": f"user::{user_id}"})
    if "Item" in response:
        return response["Item"]
    else:
        return None


def putItem(year, guild, campus, score):
    table = dynamodb.Table(os.getenv("DYNAMODB_EVENTS_TABLE_NAME"))
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


def getAverage(day: str, guild: str = None) -> float:
    """
    Get averege fiilis for the day (based on the timestamp)
    If guild is specified, get the average for the guild
    """
    table = dynamodb.Table(os.getenv("DYNAMODB_EVENTS_TABLE_NAME"))
    if guild:
        response = table.query(
            IndexName="guild-index",
            KeyConditionExpression="guild = :g",
            FilterExpression="begins_with(partition_key, :p)",
            ExpressionAttributeValues={
                ":g": guild,
                ":p": day,
            },
        )
    else:
        response = table.query(
            KeyConditionExpression="begins_with(partition_key, :p)",
            ExpressionAttributeValues={
                ":p": day,
            },
        )
    items = response["Items"]
    if items:
        return sum([int(item["score"]) for item in items]) / len(items)
    else:
        return 0
