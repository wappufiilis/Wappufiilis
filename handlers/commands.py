import datetime

from telegram import Update, constants
from telegram.ext import ContextTypes

from database.database import getUserInfo, saveUserInfo
from handlers.callbackQuery import meta_inline_menu
from keyboards import MAIN_MENU_KEYBOARD, SCORE_KEYBOARD
from messages import BASE_MESSAGE, RESULTS_MESSAGE
from utils import DatabaseKeys, KeyboardKeys


async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Need to get user data from database
    user = getUserInfo(update.message.from_user.id)
    if not user:
        user = saveUserInfo(update.message.from_user.id)
    message = BASE_MESSAGE.format(
        update.message.from_user.first_name,
    )

    await update.message.reply_photo(
        photo="https://wappufiilisweb.vercel.app/welcome.webp",
        caption=message,
        reply_markup=MAIN_MENU_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: user.get(DatabaseKeys.GUILD.value, ""),
                KeyboardKeys.CAMPUS.value: user.get(DatabaseKeys.CAMPUS.value, ""),
                KeyboardKeys.YEAR.value: user.get(DatabaseKeys.YEAR.value, ""),
                KeyboardKeys.SCORE.value: user.get(DatabaseKeys.LAST_SCORE.value, ""),
            }
        ),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    #
    # await update.message.reply_text(
    #    text=message,
    #    reply_markup=MAIN_MENU_KEYBOARD(
    #        {
    #            KeyboardKeys.GUILD.value: user.get(DatabaseKeys.GUILD.value),
    #            KeyboardKeys.CAMPUS.value: user.get(DatabaseKeys.CAMPUS.value),
    #            KeyboardKeys.YEAR.value: user.get(DatabaseKeys.YEAR.value),
    #            KeyboardKeys.SCORE.value: user.get(DatabaseKeys.LAST_SCORE.value),
    #        }
    #    ),
    #    parse_mode=constants.ParseMode.MARKDOWN_V2,
    # )
    return -1
