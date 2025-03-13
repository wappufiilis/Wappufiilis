import requests
from config import config

def put_item(year: str, guild: str, campus: str, score: int) -> int:
    """Post wellbeing score to the web frontend API"""
    data = {
        "year": year,
        "guild": guild,
        "campus": campus,
        "score": score,
    }
    response = requests.post(f"{config.WEB_BASE_URL}/api/fiilis", json=data)
    return response.status_code 