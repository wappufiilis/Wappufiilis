import os
import random
from datetime import datetime

from telegram import Update, constants
from telegram.ext import CallbackContext, ContextTypes
from telegram.helpers import escape_markdown

from keyboards import ASSOCIATION_KEYBOARD, CAMPUS_KEYBOARD, YEAR_KEYBOARD
from messages import *


async def meta_inline_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    callbackData = query.data
    if callbackData == "start":
        await query.edit_message_text(
            text=CAMPUS_SELECT,
            reply_markup=CAMPUS_KEYBOARD,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
    else:
        keyValuePairs = callbackData.split("::")
        options = {}
        for pair in keyValuePairs:
            key, value = pair.split(":")
            options[key] = value
        print("meta: inline options", options)
        if "year" in options:
            year = options["year"]

            await query.edit_message_text(
                text=ENTER_FIILIS.format(year),
                reply_markup=None,
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            )
        elif "guild" in options:
            guild = options["guild"]

            await query.edit_message_text(
                text=SELECT_YEAR.format(guild),
                reply_markup=YEAR_KEYBOARD(callbackData),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            )
        elif "campus" in options:
            campus = options["campus"]
            await query.edit_message_text(
                text=SELECT_GUILD.format(campus),
                reply_markup=ASSOCIATION_KEYBOARD(campus),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            )
