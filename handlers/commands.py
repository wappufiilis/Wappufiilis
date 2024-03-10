from telegram import Update, constants
from telegram.ext import ContextTypes

from database.database import getUserInfo, saveUserInfo
from handlers.callbackQuery import meta_inline_menu
from keyboards import SCORE_KEYBOARD
from messages import BASE_MESSAGE, RESULTS_MESSAGE
from utils import DatabaseKeys, KeyboardKeys


async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Need to get user data from database
    user = getUserInfo(update.message.from_user.id)
    if not user:
        user = saveUserInfo(update.message.from_user.id)
    await update.message.reply_text(
        text=BASE_MESSAGE.format(
            update.message.from_user.first_name,
            user.get(DatabaseKeys.GUILD.value),
            user.get(DatabaseKeys.YEAR.value),
            user.get(DatabaseKeys.LAST_SCORE.value),
        ),
        reply_markup=SCORE_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: user.get(DatabaseKeys.GUILD.value),
                KeyboardKeys.CAMPUS.value: user.get(DatabaseKeys.CAMPUS.value),
                KeyboardKeys.YEAR.value: user.get(DatabaseKeys.YEAR.value),
                KeyboardKeys.SCORE.value: user.get(DatabaseKeys.LAST_SCORE.value),
            }
        ),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return -1

async def results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Need to get user data from database
    user = getUserInfo(update.message.from_user.id)
    if not user:
        user = saveUserInfo(update.message.from_user.id)
    await update.message.reply_text(
        text=RESULTS_MESSAGE.format(4),
        reply_markup=SCORE_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: user.get(DatabaseKeys.GUILD.value),
                KeyboardKeys.CAMPUS.value: user.get(DatabaseKeys.CAMPUS.value),
                KeyboardKeys.YEAR.value: user.get(DatabaseKeys.YEAR.value),
                KeyboardKeys.SCORE.value: user.get(DatabaseKeys.LAST_SCORE.value),
            }
        ),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return -1