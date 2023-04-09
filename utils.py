def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def userToCallbackData(user: dict):
    return f"campus::{user['campus']}::guild::{user['guild']}::year::{user['year']}"
