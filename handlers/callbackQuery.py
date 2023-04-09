import json

from telegram import Update, constants
from telegram.ext import CallbackContext, ContextTypes
from telegram.helpers import escape_markdown

from database.database import putItem
from keyboards import ASSOCIATION_KEYBOARD, CAMPUS_KEYBOARD, SCORE_KEYBOARD
from messages import *
from utils import KeyboardKeys, MenuKeys, chunks, decompressCallBackData


async def meta_inline_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    callbackData = decompressCallBackData(query.data)
    print("callback data is", callbackData)
    guild = callbackData.get(KeyboardKeys.GUILD.value)
    campus = callbackData.get(KeyboardKeys.CAMPUS.value)
    year = callbackData.get(KeyboardKeys.YEAR.value)
    score = callbackData.get(KeyboardKeys.SCORE.value)
    timestamp = callbackData.get(KeyboardKeys.TIMESTAMP.value)
    newScore = callbackData.get(KeyboardKeys.NEW_SCORE.value)
    menu = callbackData.get(KeyboardKeys.MENU.value)
    if newScore:
        # Update the score
        putItem(
            year=year,
            guild=guild,
            campus=campus,
            score=newScore,
        )
        await query.edit_message_text(
            text=BASE_MESSAGE.format(
                escape_markdown(query.from_user.first_name),
                guild,
                year,
                newScore,
            ),
            reply_markup=SCORE_KEYBOARD(
                {
                    KeyboardKeys.GUILD.value: guild,
                    KeyboardKeys.CAMPUS.value: campus,
                    KeyboardKeys.YEAR.value: year,
                    "score": newScore,
                    "timestamp": timestamp,
                }
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
    elif menu == MenuKeys.CAMPUS.value:
        await query.edit_message_text(
            text=CAMPUS_SELECT,
            reply_markup=CAMPUS_KEYBOARD(
                {
                    KeyboardKeys.GUILD.value: guild,
                    KeyboardKeys.CAMPUS.value: campus,
                    KeyboardKeys.YEAR.value: year,
                    "score": newScore,
                    "timestamp": timestamp,
                }
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
    elif menu == MenuKeys.GUILD.value:
        await query.edit_message_text(
            text=SELECT_GUILD,
            reply_markup=ASSOCIATION_KEYBOARD(
                {
                    KeyboardKeys.GUILD.value: guild,
                    KeyboardKeys.CAMPUS.value: campus,
                    KeyboardKeys.YEAR.value: year,
                    "score": newScore,
                    "timestamp": timestamp,
                }
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
