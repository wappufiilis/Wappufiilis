import hashlib
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils import (
    Kampus,
    KeyboardKeys,
    Killat,
    MenuKeys,
    Vuodet,
    chunks,
    compressCallBackData,
)


def CAMPUS_KEYBOARD(callBackData: dict):
    print("got campus keyboard", callBackData)
    keyboard = list(
        chunks(
            [
                InlineKeyboardButton(
                    campus.name.lower().capitalize(),
                    callback_data=compressCallBackData(
                        {
                            KeyboardKeys.GUILD.value: callBackData[
                                KeyboardKeys.GUILD.value
                            ],
                            KeyboardKeys.CAMPUS.value: campus.value,
                            KeyboardKeys.YEAR.value: callBackData[
                                KeyboardKeys.YEAR.value
                            ],
                            KeyboardKeys.MENU.value: MenuKeys.GUILD.value,
                        }
                    ),
                )
                for campus in Kampus
            ],
            3,
        )
    )

    # Add option to go back
    keyboard.append(
        [
            InlineKeyboardButton(
                "Back",
                callback_data=compressCallBackData(
                    {
                        KeyboardKeys.GUILD.value: callBackData[
                            KeyboardKeys.GUILD.value
                        ],
                        KeyboardKeys.CAMPUS.value: callBackData[
                            KeyboardKeys.CAMPUS.value
                        ],
                        KeyboardKeys.YEAR.value: callBackData[KeyboardKeys.YEAR.value],
                    }
                ),
            ),
        ]
    )
    return InlineKeyboardMarkup(keyboard)


def ASSOCIATION_KEYBOARD(callBackData: dict):
    print("got ASSOCIATION_KEYBOARD", callBackData)

    guildButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    guild,
                    callback_data=compressCallBackData(
                        {
                            KeyboardKeys.GUILD.value: guild,
                            KeyboardKeys.CAMPUS.value: callBackData[
                                KeyboardKeys.CAMPUS.value
                            ],
                            KeyboardKeys.YEAR.value: callBackData[
                                KeyboardKeys.YEAR.value
                            ],
                        }
                    ),
                )
                for guild in Killat[callBackData[KeyboardKeys.CAMPUS.value]]
            ],
            3,
        )
    )

    # Add option to go back
    guildButtons.append(
        [
            InlineKeyboardButton(
                "Back",
                callback_data=compressCallBackData(
                    {
                        KeyboardKeys.GUILD.value: callBackData[
                            KeyboardKeys.GUILD.value
                        ],
                        KeyboardKeys.CAMPUS.value: callBackData[
                            KeyboardKeys.CAMPUS.value
                        ],
                        KeyboardKeys.YEAR.value: callBackData[KeyboardKeys.YEAR.value],
                        KeyboardKeys.MENU.value: MenuKeys.CAMPUS.value,
                    }
                ),
            ),
        ]
    )
    return InlineKeyboardMarkup(guildButtons)


def YEAR_KEYBOARD(callBackData: dict):
    print("got YEAR_KEYBOARD", callBackData)
    yearButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    year,
                    callback_data=compressCallBackData(
                        {
                            KeyboardKeys.GUILD.value: callBackData[
                                KeyboardKeys.GUILD.value
                            ],
                            KeyboardKeys.CAMPUS.value: callBackData[
                                KeyboardKeys.CAMPUS.value
                            ],
                            KeyboardKeys.YEAR.value: year,
                        }
                    ),
                )
                for year in Vuodet
            ],
            3,
        )
    )
    # Add option to go back
    yearButtons.append(
        [
            InlineKeyboardButton(
                "Back",
                callback_data=compressCallBackData(
                    {
                        KeyboardKeys.GUILD.value: callBackData[
                            KeyboardKeys.GUILD.value
                        ],
                        KeyboardKeys.CAMPUS.value: callBackData[
                            KeyboardKeys.CAMPUS.value
                        ],
                        KeyboardKeys.YEAR.value: callBackData[KeyboardKeys.YEAR.value],
                    }
                ),
            ),
        ]
    )

    return InlineKeyboardMarkup(yearButtons)


def SCORE_KEYBOARD(callBackData: dict):
    scoreButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    score,
                    callback_data=compressCallBackData(
                        {
                            KeyboardKeys.GUILD.value: callBackData[
                                KeyboardKeys.GUILD.value
                            ],
                            KeyboardKeys.CAMPUS.value: callBackData[
                                KeyboardKeys.CAMPUS.value
                            ],
                            KeyboardKeys.YEAR.value: callBackData[
                                KeyboardKeys.YEAR.value
                            ],
                            KeyboardKeys.NEW_SCORE.value: score,
                        }
                    ),
                )
                for score in range(0, 11)
            ],
            3,
        )
    )
    # Add buttons to go to guild select (campus first) and year select
    scoreButtons.append(
        [
            InlineKeyboardButton(
                "Select guild",
                callback_data=compressCallBackData(
                    {
                        KeyboardKeys.GUILD.value: callBackData[
                            KeyboardKeys.GUILD.value
                        ],
                        KeyboardKeys.CAMPUS.value: callBackData[
                            KeyboardKeys.CAMPUS.value
                        ],
                        KeyboardKeys.YEAR.value: callBackData[KeyboardKeys.YEAR.value],
                        KeyboardKeys.MENU.value: MenuKeys.CAMPUS.value,
                    }
                ),
            )
        ],
    )
    scoreButtons.append(
        [
            InlineKeyboardButton(
                "Select fuksi year",
                callback_data=compressCallBackData(
                    {
                        KeyboardKeys.GUILD.value: callBackData[
                            KeyboardKeys.GUILD.value
                        ],
                        KeyboardKeys.CAMPUS.value: callBackData[
                            KeyboardKeys.CAMPUS.value
                        ],
                        KeyboardKeys.YEAR.value: callBackData[KeyboardKeys.YEAR.value],
                        KeyboardKeys.MENU.value: MenuKeys.YEAR.value,
                    }
                ),
            ),
        ],
    )

    return InlineKeyboardMarkup(scoreButtons)
