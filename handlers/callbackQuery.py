from telegram import Update, constants
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from database.database import putItem, saveUserInfo
from keyboards import (
    ASSOCIATION_KEYBOARD,
    CAMPUS_KEYBOARD,
    SCORE_KEYBOARD,
    YEAR_KEYBOARD,
)
from messages import *
from utils import Kampus, KeyboardKeys, MenuKeys, decompressCallBackData


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
        score = newScore
        putItem(
            year=year,
            guild=guild,
            campus=campus,
            score=newScore,
        )
        saveUserInfo(
            user_id=query.from_user.id,
            campus=campus,
            guild=guild,
            year=year,
            newScore=newScore,
        )
    elif not menu:
        saveUserInfo(
            user_id=query.from_user.id,
            campus=campus,
            guild=guild,
            year=year,
        )
    if not menu:
        print("geototo", score)
        # Update the score
        await query.edit_message_text(
            text=BASE_MESSAGE.format(
                escape_markdown(query.from_user.first_name),
                guild,
                year,
                score,
            ),
            reply_markup=SCORE_KEYBOARD(
                {
                    KeyboardKeys.GUILD.value: guild,
                    KeyboardKeys.CAMPUS.value: campus,
                    KeyboardKeys.YEAR.value: year,
                    KeyboardKeys.SCORE.value: newScore,
                    KeyboardKeys.TIMESTAMP.value: timestamp,
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
                    KeyboardKeys.SCORE.value: newScore,
                    KeyboardKeys.TIMESTAMP.value: timestamp,
                }
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
    elif menu == MenuKeys.GUILD.value:
        await query.edit_message_text(
            text=SELECT_GUILD.format(
                Kampus(campus).name.lower().capitalize(),
            ),
            reply_markup=ASSOCIATION_KEYBOARD(
                {
                    KeyboardKeys.GUILD.value: guild,
                    KeyboardKeys.CAMPUS.value: campus,
                    KeyboardKeys.YEAR.value: year,
                    KeyboardKeys.SCORE.value: newScore,
                    KeyboardKeys.TIMESTAMP.value: timestamp,
                }
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
    elif menu == MenuKeys.YEAR.value:
        await query.edit_message_text(
            text=SELECT_YEAR if not guild else SELECT_YEAR_GUILD.format(guild),
            reply_markup=YEAR_KEYBOARD(
                {
                    KeyboardKeys.GUILD.value: guild,
                    KeyboardKeys.CAMPUS.value: campus,
                    KeyboardKeys.YEAR.value: year,
                    KeyboardKeys.SCORE.value: newScore,
                    KeyboardKeys.TIMESTAMP.value: timestamp,
                }
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
    elif menu == MenuKeys.RESULTS.value:
        results = 4 #getAverage(day=timestamp, guild=guild)

        await query.edit_message_text(
            text=RESULTS_MESSAGE.format(results),
            reply_markup=SCORE_KEYBOARD(
                {
                    KeyboardKeys.GUILD.value: guild,
                    KeyboardKeys.CAMPUS.value: campus,
                    KeyboardKeys.YEAR.value: year,
                    KeyboardKeys.SCORE.value: newScore,
                    KeyboardKeys.TIMESTAMP.value: timestamp,
                }
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
        )
