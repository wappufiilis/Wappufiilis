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

PerPage = 9


def CAMPUS_KEYBOARD(callBackData: dict):
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
    AllGuilds = Killat[callBackData[KeyboardKeys.CAMPUS.value]]
    maxPagination = len(AllGuilds) // PerPage
    pagination = min(
        int(callBackData.get(KeyboardKeys.PAGINATION.value, 0)), maxPagination
    )
    paginatedGuilds = AllGuilds[pagination * PerPage : (pagination + 1) * PerPage]
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
                for guild in paginatedGuilds
            ],
            3,
        )
    )
    navigationButtons = []
    if pagination > 0:
        navigationButtons.append(
            InlineKeyboardButton(
                "<<",
                callback_data=compressCallBackData(
                    {
                        **callBackData,
                        KeyboardKeys.PAGINATION.value: pagination - 1,
                        KeyboardKeys.MENU.value: MenuKeys.GUILD.value,
                    }
                ),
            )
        )
    if pagination < maxPagination:
        navigationButtons.append(
            InlineKeyboardButton(
                ">>",
                callback_data=compressCallBackData(
                    {
                        **callBackData,
                        KeyboardKeys.PAGINATION.value: pagination + 1,
                        KeyboardKeys.MENU.value: MenuKeys.GUILD.value,
                    }
                ),
            )
        )
    guildButtons.append(navigationButtons)
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
                # InlineKeyboardButton(
                #     "Today's Average",
                #     callback_data=compressCallBackData(
                #         {
                #             **callBackData,
                #             KeyboardKeys.MENU.value: MenuKeys.RESULTS.value,
                #         }
                #     ),
                # ),
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
                    f"Select campus and guild (Current: {Kampus(callBackData.get(KeyboardKeys.CAMPUS.value, 'None')).name}, {callBackData.get(KeyboardKeys.GUILD.value, 'None')})",
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
                        "Graph of Your Scores",
                        callback_data=compressCallBackData(
                            {
                                **callBackData,
                                KeyboardKeys.MENU.value: MenuKeys.GRAPH_USER.value,
                            }
                        ),
                    )
                ]
                + (
                    [
                        InlineKeyboardButton(
                            f"Graph for Your Campus {Kampus(callBackData.get(KeyboardKeys.CAMPUS.value)).name}",
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
                )
                + (
                    [
                        InlineKeyboardButton(
                            f"Graph for Your Guild {callBackData.get(KeyboardKeys.GUILD.value, 'None')}",
                            callback_data=compressCallBackData(
                                {
                                    **callBackData,
                                    KeyboardKeys.MENU.value: MenuKeys.GRAPH_GUILD.value,
                                }
                            ),
                        )
                    ]
                    if callBackData.get(KeyboardKeys.GUILD.value)
                    else []
                )
                + (
                    [
                        InlineKeyboardButton(
                            f"Graph for Your Year {callBackData.get(KeyboardKeys.YEAR.value, 'None')}",
                            callback_data=compressCallBackData(
                                {
                                    **callBackData,
                                    KeyboardKeys.MENU.value: MenuKeys.GRAPH_YEAR.value,
                                }
                            ),
                        )
                    ]
                    if callBackData.get(KeyboardKeys.YEAR.value)
                    else []
                )
                + [
                    InlineKeyboardButton(
                        "Back",
                        callback_data=compressCallBackData(
                            {
                                **callBackData,
                            }
                        ),
                    ),
                ]
            ),
            1,
        )
    )
    return InlineKeyboardMarkup(personalInfoButtons)
