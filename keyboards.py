import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils import chunks

OK_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Ok", callback_data="delete"),
        ],
    ]
)


def CAMPUS_KEYBOARD(user):
    baseCallback = (
        f"campus::{user['campus']}::guild::{user['guild']}::year::{user['year']}"
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Otaniemi", callback_data="campus:Aalto"),
                InlineKeyboardButton("Tampere", callback_data="campus:Tampere"),
            ],
            [
                InlineKeyboardButton("Turku", callback_data="campus:Turku"),
                InlineKeyboardButton("lappeen Ranta", callback_data="campus:LUT"),
            ],
            [
                InlineKeyboardButton("Jyväskylä", callback_data="campus:Jyväskylä"),
                InlineKeyboardButton("Oulu", callback_data="campus:Oulu"),
            ],
        ]
    )


Killat = {
    "Aalto": [
        "SIK",
        "AK",
        "AS",
        "Athene",
        "DG",
        "FK",
        "Inkubio",
        "KIK",
        "MK",
        "Prodeko",
        "PJK",
        "IK",
        "TiK",
        "VK",
        "KK",
        "TF",
    ],
    "LUT": [
        "Armatuuri",
        "Cluster",
        "Kaplaaki",
        "KeTeK",
        "KRK",
        "Lateksii",
        "Pelletti",
        "Sätky",
    ],
    "Oulu": [
        "OPTIEM",
        "Arkkitehtikilta",
        "Konekilta",
        "Prosessikilta",
        "OTiT",
        "Ympäristörakentajakilta",
        "SIK",
    ],
    "Tampere": [
        "Arkkitehtikilta",
        "Autek",
        "Bioner",
        "Indecs",
        "INTO",
        "KoRK",
        "MIK",
        "TARAKI",
        "Skilta",
        "Hiukkanen",
        "Man@ger",
        "TiTe",
        "Urbanum",
        "YKI",
    ],
    "Turku": [
        "Adamas",
        "Asklepio",
        "Digit",
        "Machina",
        "Nucleus",
        "Kemistklubben",
        "DaTe",
    ],
    "Vaasa": ["Tutti ry"],
    "Jyväskylä": [
        "Algo",
    ],
}


def ASSOCIATION_KEYBOARD(campus: str):
    guildButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    guild,
                    callback_data=f"campus:{campus}::guild:{guild}",
                )
                for guild in Killat[campus]
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


Vuodet = [
    "aNcient",
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
]


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
    print("callback data is", callBackData)
    data_json = json.dumps(callBackData)

    print(f"Size of JSON string: {len(data_json)} bytes")
    scoreButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    score,
                    callback_data=json.dumps(
                        {
                            **callBackData,
                            "newScore": score,
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
                callback_data=json.dumps({**callBackData, "menu": "guild"}),
            )
        ],
    )
    scoreButtons.append(
        [
            InlineKeyboardButton(
                "Select fuksi year",
                callback_data=json.dumps({**callBackData, "menu": "year"}),
            ),
        ],
    )

    # remove the last pair from callbackData
    return InlineKeyboardMarkup(scoreButtons)
