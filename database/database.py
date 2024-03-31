import os
import random
from datetime import datetime

import boto3
from botocore.credentials import Credentials

from utils import DatabaseKeys

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
    newScore: str = None,
):
    """
    Save user info, if user already exists, update the info
    """
    table = dynamodb.Table(os.getenv("DYNAMODB_USERS_TABLE_NAME"))
    user = {}
    if newScore:
        user = getUserInfo(user_id)
        table.update_item(
            Key={"user_id": str(user_id)},
            UpdateExpression="set last_score=:s, scores=:sc",
            ExpressionAttributeValues={
                ":s": newScore,
                ":sc": user.get(DatabaseKeys.SCORES.value, []) + [newScore],
            },
            ReturnValues="NONE",
        )
    else:
        table.update_item(
            Key={"user_id": str(user_id)},
            UpdateExpression="set campus=:c, guild=:g, study_year=:y",
            ExpressionAttributeValues={
                ":c": campus,
                ":g": guild,
                ":y": year,
            },
            ReturnValues="NONE",
        )
    return user


def getUserInfo(user_id: str) -> dict:
    """
    Get user info
    If no user exists, return None
    """
    table = dynamodb.Table(os.getenv("DYNAMODB_USERS_TABLE_NAME"))
    try:
        response = table.get_item(Key={"user_id": str(user_id)})
    except Exception as e:
        return None
    if "Item" in response:
        return response["Item"]
    else:
        return None


def putItem(user_id, year, guild, campus, score):
    timestamp = int(datetime.now().timestamp())
    datestring = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

    perUserTable = dynamodb.Table(os.getenv("DYNAMODB_EVENTS_TABLE_NAME"))
    perUserTable.put_item(
        Item={
            "partition_key": f"{user_id}::{datestring}",
            "year": year,
            "guild": guild,
            "campus": campus,
            "score": score,
            "timestamp": timestamp,
        }
    )

    if guild is not None and campus is not None:
        perGuildTable = dynamodb.Table(
            os.getenv("DYNAMODB_EVENTS_PER_GUILD_TABLE_NAME")
        )
        perGuildTable.put_item(
            Item={
                "partition_key": f"{campus}::{guild}::{year}::{user_id}::{datestring}",
                "year": year,
                "campus": campus,
                "score": score,
                "timestamp": timestamp,
                "user_id": user_id,
            }
        )
    if year is not None:
        perYearTable = dynamodb.Table(os.getenv("DYNAMODB_EVENTS_PER_YEAR_TABLE_NAME"))
        perYearTable.put_item(
            Item={
                "partition_key": f"{year}::{campus}::{guild}::{user_id}::{datestring}",
                "year": year,
                "campus": campus,
                "score": score,
                "timestamp": timestamp,
                "user_id": user_id,
            }
        )


def getDayAverage(day: str) -> float:
    """
    Get averege fiilis for the day (based on the timestamp)

    params:
    day: str - date in format "YYYY-MM-DD"
    """
    start_of_day = int(
        datetime.strptime(day, "%Y-%m-%d")
        .replace(hour=0, minute=0, second=0)
        .timestamp()
    )
    end_of_day = int(
        datetime.strptime(day, "%Y-%m-%d")
        .replace(hour=23, minute=59, second=59)
        .timestamp()
    )

    table = dynamodb.Table(os.getenv("DYNAMODB_EVENTS_TABLE_NAME"))

    # Use sort index "timestamp" to get all items for the day
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr("timestamp").between(
            start_of_day, end_of_day
        )
    )

    items = response["Items"]
    if items:
        return sum([int(item["score"]) for item in items]) / len(items)
    else:
        return 0
