import os
import random
from datetime import datetime

from telegram import Update, constants
from telegram.ext import CallbackContext, ContextTypes
from telegram.helpers import escape_markdown

from keyboards import ASSOCIATION_KEYBOARD, CAMPUS_KEYBOARD
from messages import *


async def meta_inline_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    options = query.data.split(":")
    print("meta inline options", options)
    selected = options[0]
    if selected == "campusSelect":
        await query.edit_message_text(
            text=CAMPUS_SELECT,
            reply_markup=CAMPUS_KEYBOARD,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
    if selected == "campusSelected":
        campus = options[1]
        await query.edit_message_text(
            text=CAMPUS_SELECTED.format(campus),
            reply_markup=ASSOCIATION_KEYBOARD(campus),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
