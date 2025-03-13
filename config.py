from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # AWS Configuration
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_DEFAULT_REGION: str = os.getenv("AWS_DEFAULT_REGION", "eu-west-1")
    
    # DynamoDB Tables
    DYNAMODB_USERS_TABLE_NAME: str = os.getenv("DYNAMODB_USERS_TABLE_NAME", "")
    DYNAMODB_EVENTS_TABLE_NAME: str = os.getenv("DYNAMODB_EVENTS_TABLE_NAME", "")
    DYNAMODB_EVENTS_PER_GUILD_TABLE_NAME: str = os.getenv("DYNAMODB_EVENTS_PER_GUILD_TABLE_NAME", "")
    DYNAMODB_EVENTS_PER_YEAR_TABLE_NAME: str = os.getenv("DYNAMODB_EVENTS_PER_YEAR_TABLE_NAME", "")
    
    # Telegram Configuration
    TELEGRAM_TOKEN: str = os.getenv("TOKEN", "")
    
    # Application Configuration
    TIMEZONE: str = os.getenv("TIMEZONE", "Europe/Helsinki")
    
    # Web Configuration
    WEB_BASE_URL: str = "https://wappufiilisweb.vercel.app"

config = Config() 