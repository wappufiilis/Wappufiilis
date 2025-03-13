from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class DatabaseKeys(str, Enum):
    USER_ID = "user_id"
    GUILD = "guild"
    CAMPUS = "campus"
    YEAR = "study_year"
    TIMESTAMP = "timestamp"
    LAST_SCORE = "last_score"
    SCORES = "scores"

class User(BaseModel):
    user_id: str
    campus: Optional[str] = ""
    guild: Optional[str] = ""
    study_year: Optional[str] = ""
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def to_dict(self) -> dict:
        """Convert to dictionary with original database keys"""
        return {
            DatabaseKeys.USER_ID: self.user_id,
            DatabaseKeys.CAMPUS: self.campus,
            DatabaseKeys.GUILD: self.guild,
            DatabaseKeys.YEAR: self.study_year,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

class WellbeingScore(BaseModel):
    partition_key: str  # Format: "{user_id}::{datestring}"
    year: Optional[str] = ""
    guild: Optional[str] = ""
    campus: Optional[str] = ""
    score: int
    timestamp: int  # Unix timestamp for the date
    ts_exact: int  # Exact timestamp of submission
    timezone: str

class GuildScore(BaseModel):
    partition_key: str  # Format: "{campus}::{guild}::{year}::{user_id}::{datestring}"
    year: str
    campus: str
    score: int
    timestamp: int
    ts_exact: int
    timezone: str
    user_id: str

class YearScore(BaseModel):
    partition_key: str  # Format: "{year}::{campus}::{guild}::{user_id}::{datestring}"
    year: str
    campus: str
    score: int
    timestamp: int
    ts_exact: int
    timezone: str
    user_id: str 