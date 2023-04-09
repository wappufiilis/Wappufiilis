import os
import random
from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")


def saveUserInfo(user_id: str, campus: str = None, guild: str = None, year: str = None):
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
        }
    )


def getUserInfo(user_id: str):
    """
    Get user info
    If no user exists, return None
    """
    table = dynamodb.Table(os.getenv("DYNAMODB_USERS_TABLE_NAME"))
    response = table.get_item(Key={"partition_key": f"user::{user_id}"})
    if "Item" in response:
        return response["Item"]
    else:
        return None


def putItem(year, guild, score):
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


def getAverage(day: str, guild: str = None):
    """
    Get averege fiilis for the day (based on the timestamp)
    If guild is specified, get the average for the guild
    """
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE_NAME"))
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
