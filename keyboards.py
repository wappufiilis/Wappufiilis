from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils import chunks

OK_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Ok", callback_data="delete"),
        ],
    ]
)


CAMPUS_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Otaniemi", callback_data="campusSelected:Aalto"),
            InlineKeyboardButton("Tampere", callback_data="campusSelected:Tampere"),
        ],
        [
            InlineKeyboardButton("Turku", callback_data="campusSelected:Turku"),
            InlineKeyboardButton("lappeen Ranta", callback_data="campusSelected:LUT"),
        ],
        [
            InlineKeyboardButton("Jyväskylä", callback_data="campusSelected:Jyväskylä"),
            InlineKeyboardButton("Oulu", callback_data="campusSelected:Oulu"),
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


def ASSOCIATION_KEYBOARD(university: str):
    guildButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    association,
                    callback_data=f"associationSelected:{association}",
                )
                for association in Killat[university]
            ],
            3,
        )
    )

    guildButtons.append(
        [
            InlineKeyboardButton("Back", callback_data="campusSelect:back"),
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


def YEAR_KEYBOARD():
    yearButtons = list(
        chunks(
            [
                InlineKeyboardButton(
                    year,
                    callback_data=f"yearSelected:{year}",
                )
                for year in Vuodet
            ],
            3,
        )
    )
    yearButtons.append(
        [
            InlineKeyboardButton("Back", callback_data="campusSelect:back"),
        ]
    )

    return InlineKeyboardMarkup(yearButtons)
