from telegram import Update, constants
from telegram.ext import ContextTypes

from handlers.callbackQuery import meta_inline_menu
from keyboards import CAMPUS_KEYBOARD
from messages import GREETING_NEW


async def home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text=GREETING_NEW.format(update.message.from_user.first_name),
        reply_markup=CAMPUS_KEYBOARD,
        parse_mode=constants.ParseMode.MARKDOWN_V2,
    )
    return -1
