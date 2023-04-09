from telegram import Update, constants
from telegram.ext import ContextTypes

from database.database import getUserInfo
from handlers.callbackQuery import meta_inline_menu
from keyboards import SCORE_KEYBOARD
from messages import BASE_MESSAGE
from utils import userToCallbackData


async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Need to get user data from database
    user = getUserInfo(update.message.from_user.id)
    await update.message.reply_text(
        text=BASE_MESSAGE.format(
            update.message.from_user.first_name,
            user["guild"],
            user["year"],
            user["lastWappuFiilis"],
        ),
        reply_markup=SCORE_KEYBOARD(user),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return -1
