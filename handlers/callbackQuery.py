from telegram import Update, constants
from telegram.ext import CallbackContext, ContextTypes
from telegram.helpers import escape_markdown

from database.database import putItem
from keyboards import (
    ASSOCIATION_KEYBOARD,
    CAMPUS_KEYBOARD,
    SCORE_KEYBOARD,
    YEAR_KEYBOARD,
)
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
        # create new callbackData string, drop all keys that start with "new" or "edit"
        callbackData = "::".join(
            [
                pair
                for pair in keyValuePairs
                if not pair.startswith("new") and not pair.startswith("edit")
            ]
        )
        options = {}
        for pair in keyValuePairs:
            key, value = pair.split(":")
            options[key] = value
        print("meta: inline options", options)
        if "newScore" in options:
            putItem(options["year"], options["guild"], options["newScore"])
            await query.edit_message_text(
                text=GREETING_NEW.format(
                    options["year"],
                    options["guild"],
                    options["newScore"],
                ),
                reply_markup=SCORE_KEYBOARD(callbackData),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            )
        elif "year" in options:
            year = options["year"]
            await query.edit_message_text(
                text=GREETING_NEW.format(
                    options["year"],
                    options["guild"],
                ),
                reply_markup=SCORE_KEYBOARD(callbackData),
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
