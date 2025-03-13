import boto3
from botocore.credentials import Credentials
from typing import Optional, List, Dict
import pytz
from datetime import datetime

from config import config
from .models import User, WellbeingScore, GuildScore, YearScore, DatabaseKeys
from exceptions import DatabaseError
from .api_interface import put_item

class DynamoDBClient:
    def __init__(self):
        creds = Credentials(
            access_key=config.AWS_ACCESS_KEY_ID,
            secret_key=config.AWS_SECRET_ACCESS_KEY,
        )
        self.client = boto3.client(
            "dynamodb",
            region_name=config.AWS_DEFAULT_REGION,
            aws_access_key_id=creds.access_key,
            aws_secret_access_key=creds.secret_key,
        )
        self.dynamodb = boto3.resource("dynamodb", region_name=config.AWS_DEFAULT_REGION)
        self.users_table = self.dynamodb.Table(config.DYNAMODB_USERS_TABLE_NAME)
        self.events_table = self.dynamodb.Table(config.DYNAMODB_EVENTS_TABLE_NAME)
        self.guild_events_table = self.dynamodb.Table(config.DYNAMODB_EVENTS_PER_GUILD_TABLE_NAME)
        self.year_events_table = self.dynamodb.Table(config.DYNAMODB_EVENTS_PER_YEAR_TABLE_NAME)

    def save_user_info(self, user: User) -> Dict:
        """Save or update user information"""
        try:
            user_dict = user.to_dict()
            self.users_table.update_item(
                Key={DatabaseKeys.USER_ID: str(user.user_id)},
                UpdateExpression="set campus=:c, guild=:g, study_year=:y, updated_at=:u",
                ExpressionAttributeValues={
                    ":c": user_dict[DatabaseKeys.CAMPUS],
                    ":g": user_dict[DatabaseKeys.GUILD],
                    ":y": user_dict[DatabaseKeys.YEAR],
                    ":u": user_dict["updated_at"],
                },
                ReturnValues="NONE",
            )
            return user_dict
        except Exception as e:
            raise DatabaseError(f"Failed to save user info: {str(e)}")

    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """Get user information"""
        try:
            response = self.users_table.get_item(
                Key={DatabaseKeys.USER_ID: str(user_id)}
            )
            if "Item" in response:
                return response["Item"]
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to get user info: {str(e)}")

    def get_users(self) -> List[Dict]:
        """Get all users"""
        try:
            response = self.users_table.scan()
            return response["Items"]
        except Exception as e:
            raise DatabaseError(f"Failed to get users: {str(e)}")

    def save_wellbeing_score(self, user_id: str, year: str, guild: str, campus: str, score: int) -> None:
        """Save a new wellbeing score and related data"""
        try:
            timezone = pytz.timezone(config.TIMEZONE)
            timestamp = int(datetime.now(timezone).timestamp())
            datestring = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            timestamp_of_date = int(datetime.strptime(datestring, "%Y-%m-%d").timestamp())

            # Save main score
            main_score = WellbeingScore(
                partition_key=f"{user_id}::{datestring}",
                year=year,
                guild=guild,
                campus=campus,
                score=score,
                timestamp=timestamp_of_date,
                ts_exact=timestamp,
                timezone=str(timezone)
            )
            self.events_table.put_item(Item=main_score.dict())

            # Save guild-specific score if guild and campus are provided
            if guild and campus:
                guild_score = GuildScore(
                    partition_key=f"{campus}::{guild}::{year}::{user_id}::{datestring}",
                    year=year,
                    campus=campus,
                    score=score,
                    timestamp=timestamp_of_date,
                    ts_exact=timestamp,
                    timezone=str(timezone),
                    user_id=user_id
                )
                self.guild_events_table.put_item(Item=guild_score.dict())

            # Save year-specific score if year is provided
            if year:
                year_score = YearScore(
                    partition_key=f"{year}::{campus}::{guild}::{user_id}::{datestring}",
                    year=year,
                    campus=campus,
                    score=score,
                    timestamp=timestamp_of_date,
                    ts_exact=timestamp,
                    timezone=str(timezone),
                    user_id=user_id
                )
                self.year_events_table.put_item(Item=year_score.dict())

            # Update web frontend
            put_item(year=year, guild=guild, campus=campus, score=score)

        except Exception as e:
            raise DatabaseError(f"Failed to save wellbeing score: {str(e)}")

    def get_day_average(self, day: str) -> float:
        """Get average wellbeing score for a specific day"""
        try:
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

            response = self.events_table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr("timestamp").between(
                    start_of_day, end_of_day
                )
            )

            items = response["Items"]
            if items:
                return sum([int(item["score"]) for item in items]) / len(items)
            return 0.0
        except Exception as e:
            raise DatabaseError(f"Failed to get day average: {str(e)}")

# Create singleton instance
db = DynamoDBClient()

# Maintain original function names for compatibility
def saveUserInfo(user_id: str, campus: str = "", guild: str = "", year: str = "") -> Dict:
    user = User(user_id=user_id, campus=campus, guild=guild, study_year=year)
    return db.save_user_info(user)

def getUserInfo(user_id: str) -> Optional[Dict]:
    return db.get_user_info(user_id)

def getUsers() -> List[Dict]:
    return db.get_users()

def putItem(user_id: str, year: str, guild: str, campus: str, score: int) -> None:
    db.save_wellbeing_score(user_id, year, guild, campus, score)

def getDayAverage(day: str) -> float:
    return db.get_day_average(day)
