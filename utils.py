from enum import Enum


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def userToCallbackData(user: dict):
    dataString = (
        f"campus::{user['campus']}::guild::{user['guild']}::year::{user['year']}"
    )
    print("data string is", dataString)
    return json.dumps(user)


class KeyboardKeys(Enum):
    USER_ID = "1"
    GUILD = "2"
    CAMPUS = "3"
    YEAR = "4"
    SCORE = "5"
    TIMESTAMP = "6"
    NEW_SCORE = "7"
    MENU = "8"
