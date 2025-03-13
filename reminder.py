import asyncio
import datetime

from telegram import constants

from bot import application
from database.database import getUsers
from keyboards import MAIN_MENU_KEYBOARD
from messages import REMINDER_MESSAGE
from utils import DatabaseKeys, KeyboardKeys


async def reminder():
    users = getUsers()

    users_with_reminder = [
        user for user in users if "reminder" in user and user["reminder"] is not None
    ]

    for user in users_with_reminder:
        reminder_time = datetime.datetime.strptime(user["reminder"], "%H:%M").time()
        current_time_by_minute = (
            datetime.datetime.now().time().replace(second=0, microsecond=0)
        )
        if reminder_time == current_time_by_minute:
            await application.bot.send_photo(
                chat_id=user["user_id"],
                photo="https://wappufiilisweb.vercel.app/welcome.webp",
                caption=REMINDER_MESSAGE,
                reply_markup=MAIN_MENU_KEYBOARD(
                    {
                        KeyboardKeys.GUILD.value: user.get(
                            DatabaseKeys.GUILD.value, ""
                        ),
                        KeyboardKeys.CAMPUS.value: user.get(
                            DatabaseKeys.CAMPUS.value, ""
                        ),
                        KeyboardKeys.YEAR.value: user.get(DatabaseKeys.YEAR.value, ""),
                        KeyboardKeys.SCORE.value: user.get(
                            DatabaseKeys.LAST_SCORE.value, ""
                        ),
                    }
                ),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            )


def lambda_handler(event, context):
    asyncio.run(reminder())


if __name__ == "__main__":
    asyncio.run(reminder())
