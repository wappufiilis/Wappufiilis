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
                            **callBackData,
                            KeyboardKeys.CAMPUS.value: campus.value,
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
                        **callBackData,
                        KeyboardKeys.MENU.value: MenuKeys.PERSONAL_INFO.value,
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
                            **callBackData,
                            KeyboardKeys.GUILD.value: guild,
                            KeyboardKeys.MENU.value: MenuKeys.PERSONAL_INFO.value,
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
                        **callBackData,
                        KeyboardKeys.MENU.value: MenuKeys.PERSONAL_INFO.value,
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
                            **callBackData,
                            KeyboardKeys.YEAR.value: year,
                            KeyboardKeys.MENU.value: MenuKeys.PERSONAL_INFO.value,
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
                        **callBackData,
                        KeyboardKeys.MENU.value: MenuKeys.PERSONAL_INFO.value,
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
                            **callBackData,
                            KeyboardKeys.NEW_SCORE.value: score,
                        }
                    ),
                )
                for score in range(0, 11)
            ],
            3,
        ),
    )

    scoreButtons.append(
        [
            InlineKeyboardButton(
                "Back",
                callback_data=compressCallBackData(
                    {
                        **callBackData,
                    }
                ),
            ),
        ]
    )
    return InlineKeyboardMarkup(scoreButtons)


def MAIN_MENU_KEYBOARD(callBackData: dict):
    mainMenuButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    "Enter score",
                    callback_data=compressCallBackData(
                        {
                            **callBackData,
                            KeyboardKeys.MENU.value: MenuKeys.SCORE.value,
                        }
                    ),
                ),
                InlineKeyboardButton(
                    "Personal info",
                    callback_data=compressCallBackData(
                        {
                            **callBackData,
                            KeyboardKeys.MENU.value: MenuKeys.PERSONAL_INFO.value,
                        }
                    ),
                ),
                InlineKeyboardButton(
                    "Today's Average",
                    callback_data=compressCallBackData(
                        {
                            **callBackData,
                            KeyboardKeys.MENU.value: MenuKeys.RESULTS.value,
                        }
                    ),
                ),
                InlineKeyboardButton(
                    "Graphs",
                    callback_data=compressCallBackData(
                        {
                            **callBackData,
                            KeyboardKeys.MENU.value: MenuKeys.GRAPH.value,
                        }
                    ),
                ),
            ],
            1,
        )
    )
    return InlineKeyboardMarkup(mainMenuButtons)


def PERSONAL_INFO_KEYBOARD(callBackData: dict):
    personalInfoButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    f"Select campus and guild (Current: {callBackData.get(KeyboardKeys.CAMPUS.value, 'None')}, {callBackData.get(KeyboardKeys.GUILD.value, 'None')})",
                    callback_data=compressCallBackData(
                        {
                            **callBackData,
                            KeyboardKeys.MENU.value: MenuKeys.CAMPUS.value,
                        }
                    ),
                ),
                # InlineKeyboardButton(
                #    "Select guild",
                #    callback_data=compressCallBackData(
                #        {
                #            **callBackData,
                #            KeyboardKeys.MENU.value: MenuKeys.GUILD.value,
                #        }
                #    ),
                # ),
                InlineKeyboardButton(
                    f"Select fuksi year (Current: {callBackData.get(KeyboardKeys.YEAR.value, 'None')})",
                    callback_data=compressCallBackData(
                        {
                            **callBackData,
                            KeyboardKeys.MENU.value: MenuKeys.YEAR.value,
                        }
                    ),
                ),
                InlineKeyboardButton(
                    "Back",
                    callback_data=compressCallBackData(
                        {
                            **callBackData,
                        }
                    ),
                ),
            ],
            1,
        )
    )
    return InlineKeyboardMarkup(personalInfoButtons)


def GRAPH_KEYBOARD(callBackData: dict):
    personalInfoButtons = list(
        chunks(
            (
                [
                    InlineKeyboardButton(
                        "Back",
                        callback_data=compressCallBackData(
                            {
                                **callBackData,
                            }
                        ),
                    ),
                ]
                + [
                    InlineKeyboardButton(
                        f"Graph for Your Campus {callBackData.get(KeyboardKeys.CAMPUS.value, 'None')}",
                        callback_data=compressCallBackData(
                            {
                                **callBackData,
                                KeyboardKeys.MENU.value: MenuKeys.GRAPH_CAMPUS.value,
                            }
                        ),
                    )
                ]
                if callBackData.get(KeyboardKeys.CAMPUS.value)
                else []
            ),
            1,
        )
    )
    return InlineKeyboardMarkup(personalInfoButtons)
