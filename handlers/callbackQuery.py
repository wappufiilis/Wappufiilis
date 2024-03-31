import datetime

from telegram import InputMediaPhoto, Update, constants
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from database.database import getDayAverage, putItem, saveUserInfo
from keyboards import (
    ASSOCIATION_KEYBOARD,
    CAMPUS_KEYBOARD,
    GRAPH_KEYBOARD,
    MAIN_MENU_KEYBOARD,
    PERSONAL_INFO_KEYBOARD,
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
            user_id=query.from_user.id,
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
        keyboard = MAIN_MENU_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: guild,
                KeyboardKeys.CAMPUS.value: campus,
                KeyboardKeys.YEAR.value: year,
                KeyboardKeys.SCORE.value: newScore,
                KeyboardKeys.TIMESTAMP.value: timestamp,
            }
        )
        await query.edit_message_media(
            media=InputMediaPhoto(
                media="https://wappufiilisweb.vercel.app/welcome.webp"
            ),
            reply_markup=keyboard,
        )
        await query.edit_message_caption(
            caption=BASE_MESSAGE.format(
                escape_markdown(query.from_user.first_name),
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )

    elif menu == MenuKeys.CAMPUS.value:
        keyboard = CAMPUS_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: guild,
                KeyboardKeys.CAMPUS.value: campus,
                KeyboardKeys.YEAR.value: year,
                KeyboardKeys.SCORE.value: newScore,
                KeyboardKeys.TIMESTAMP.value: timestamp,
            }
        )
        await query.edit_message_media(
            media=InputMediaPhoto(
                media="https://wappufiilisweb.vercel.app/welcome.webp"
            ),
            reply_markup=keyboard,
        )
        await query.edit_message_caption(
            caption=CAMPUS_SELECT,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
    elif menu == MenuKeys.GUILD.value:
        keyboard = ASSOCIATION_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: guild,
                KeyboardKeys.CAMPUS.value: campus,
                KeyboardKeys.YEAR.value: year,
                KeyboardKeys.SCORE.value: newScore,
                KeyboardKeys.TIMESTAMP.value: timestamp,
            }
        )
        await query.edit_message_media(
            media=InputMediaPhoto(
                media="https://wappufiilisweb.vercel.app/guild_select.webp"
            ),
            reply_markup=keyboard,
        )
        await query.edit_message_caption(
            caption=SELECT_GUILD.format(
                Kampus(campus).name.lower().capitalize(),
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
    elif menu == MenuKeys.YEAR.value:
        keyboard = YEAR_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: guild,
                KeyboardKeys.CAMPUS.value: campus,
                KeyboardKeys.YEAR.value: year,
                KeyboardKeys.SCORE.value: newScore,
                KeyboardKeys.TIMESTAMP.value: timestamp,
            }
        )
        await query.edit_message_media(
            media=InputMediaPhoto(
                media="https://wappufiilisweb.vercel.app/fucks_year.webp"
            ),
            reply_markup=keyboard,
        )
        await query.edit_message_caption(
            caption=SELECT_YEAR if not guild else SELECT_YEAR_GUILD.format(guild),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
    elif menu == MenuKeys.RESULTS.value:
        # Convert timestamp to format YYYY-MM-DD
        day = datetime.datetime.now().strftime("%Y-%m-%d")
        average = getDayAverage(day=day)
        keyboard = MAIN_MENU_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: guild,
                KeyboardKeys.CAMPUS.value: campus,
                KeyboardKeys.YEAR.value: year,
                KeyboardKeys.SCORE.value: newScore,
                KeyboardKeys.TIMESTAMP.value: timestamp,
            }
        )
        await query.edit_message_media(
            media=InputMediaPhoto(
                media="https://wappufiilisweb.vercel.app/welcome.webp"
            ),
            reply_markup=keyboard,
        )
        await query.edit_message_caption(
            caption=RESULTS_MESSAGE.format(
                str(average).replace(".", ","),
                parse_mode=constants.ParseMode.MARKDOWN_V2,
            ),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
    elif menu == MenuKeys.PERSONAL_INFO.value:
        keyboard = PERSONAL_INFO_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: guild,
                KeyboardKeys.CAMPUS.value: campus,
                KeyboardKeys.YEAR.value: year,
                KeyboardKeys.SCORE.value: newScore,
                KeyboardKeys.TIMESTAMP.value: timestamp,
            }
        )
        await query.edit_message_media(
            media=InputMediaPhoto(
                media="https://wappufiilisweb.vercel.app/personal_info.webp"
            ),
            reply_markup=keyboard,
        )
        await query.edit_message_caption(
            caption=PERSONAL_INFO,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
    elif menu == MenuKeys.SCORE.value:
        keyboard = SCORE_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: guild,
                KeyboardKeys.CAMPUS.value: campus,
                KeyboardKeys.YEAR.value: year,
                KeyboardKeys.SCORE.value: newScore,
                KeyboardKeys.TIMESTAMP.value: timestamp,
            }
        )
        await query.edit_message_media(
            media=InputMediaPhoto(
                media="https://wappufiilisweb.vercel.app/measure.webp"
            ),
            reply_markup=keyboard,
        )
        await query.edit_message_caption(
            caption=SCORE_MESSAGE,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
    elif menu == MenuKeys.GRAPH.value:
        keyboard = GRAPH_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: guild,
                KeyboardKeys.CAMPUS.value: campus,
                KeyboardKeys.YEAR.value: year,
                KeyboardKeys.SCORE.value: newScore,
                KeyboardKeys.TIMESTAMP.value: timestamp,
            }
        )
        current_hour = datetime.datetime.now().strftime("%Y-%m-%d-%H")
        image_url = f"https://wappufiilisweb.vercel.app/kappura/{current_hour}"
        await query.edit_message_media(
            media=InputMediaPhoto(media=image_url),
            reply_markup=keyboard,
        )
        await query.edit_message_caption(
            caption=GRAPH_MESSAGE,
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
    elif menu == MenuKeys.GRAPH_CAMPUS.value:
        keyboard = GRAPH_KEYBOARD(
            {
                KeyboardKeys.GUILD.value: guild,
                KeyboardKeys.CAMPUS.value: campus,
                KeyboardKeys.YEAR.value: year,
                KeyboardKeys.SCORE.value: newScore,
                KeyboardKeys.TIMESTAMP.value: timestamp,
            }
        )
        current_hour = datetime.datetime.now().strftime("%Y-%m-%d-%H")
        image_url = (
            f"https://wappufiilisweb.vercel.app/kappura/{current_hour}/campus/{campus}"
        )
        print(image_url)
        await query.edit_message_media(
            media=InputMediaPhoto(media=image_url),
            reply_markup=keyboard,
        )
        await query.edit_message_caption(
            caption=GRAPH_MESSAGE_CAMPUS.format(Kampus(campus).name),
            parse_mode=constants.ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
