import hashlib
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils import Kampus, KeyboardKeys, Killat, Vuodet, chunks, encodeDarkMagic

OK_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Ok", callback_data="delete"),
        ],
    ]
)


def CAMPUS_KEYBOARD(callBackData: dict):
    keyboard = list(
        chunks(
            [
                [
                    InlineKeyboardButton(
                        campus.name.lower().capitalize(),
                        callback_data=encodeDarkMagic(
                            {
                                KeyboardKeys.GUILD.value: callBackData["guild"],
                                KeyboardKeys.CAMPUS.value: campus.value,
                                KeyboardKeys.YEAR.value: callBackData["year"],
                                KeyboardKeys.MENU.value: "guild",
                            }
                        ),
                    )
                    for campus in Kampus
                ]
            ],
            3,
        )
    )

    # Add option to go back
    keyboard.append(
        [
            InlineKeyboardButton(
                "Back",
                callback_data=encodeDarkMagic(callBackData),
            ),
        ]
    )
    return InlineKeyboardMarkup(keyboard)


def ASSOCIATION_KEYBOARD(callBackData: dict):
    guildButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    guild,
                    callback_data=encodeDarkMagic(
                        {
                            KeyboardKeys.GUILD.value: guild,
                            KeyboardKeys.CAMPUS.value: callBackData[
                                KeyboardKeys.CAMPUS.value
                            ],
                        }
                    ),
                )
                for guild in Killat[callBackData[KeyboardKeys.CAMPUS.value]]
            ],
            3,
        )
    )

    guildButtons.append(
        [
            InlineKeyboardButton("Back", callback_data="start"),
        ]
    )
    return InlineKeyboardMarkup(guildButtons)


def YEAR_KEYBOARD(callBackData: str):
    yearButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    year,
                    callback_data=f"{callBackData}::year:{year}",
                )
                for year in Vuodet
            ],
            3,
        )
    )
    # remove the last pair from callbackData
    goBackData = "::".join(callBackData.split("::")[:-1])
    yearButtons.append(
        [
            InlineKeyboardButton("Back", callback_data=goBackData),
        ]
    )

    return InlineKeyboardMarkup(yearButtons)


def SCORE_KEYBOARD(callBackData: dict):
    scoreButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    score,
                    callback_data=encodeDarkMagic(
                        {
                            KeyboardKeys.GUILD.value: callBackData["guild"],
                            KeyboardKeys.CAMPUS.value: callBackData["campus"],
                            KeyboardKeys.YEAR.value: callBackData["year"],
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
                callback_data=encodeDarkMagic(
                    {
                        KeyboardKeys.GUILD.value: callBackData["guild"],
                        KeyboardKeys.CAMPUS.value: callBackData["campus"],
                        KeyboardKeys.YEAR.value: callBackData["year"],
                        KeyboardKeys.MENU.value: "campus",
                    }
                ),
            )
        ],
    )
    scoreButtons.append(
        [
            InlineKeyboardButton(
                "Select fuksi year",
                callback_data=encodeDarkMagic(
                    {
                        KeyboardKeys.GUILD.value: callBackData["guild"],
                        KeyboardKeys.CAMPUS.value: callBackData["campus"],
                        KeyboardKeys.YEAR.value: callBackData["year"],
                        KeyboardKeys.MENU.value: "year",
                    }
                ),
            ),
        ],
    )

    # remove the last pair from callbackData
    return InlineKeyboardMarkup(scoreButtons)
