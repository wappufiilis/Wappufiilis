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
        "Sähköinsinöörikilta (SIK)",
        "Arkkitehtikilta (AK)",
        "AS",
        "Athene",
        "Data Guild (DG)",
        "Fyysikkokilta (FK)",
        "Inkubio",
        "Koneinsinöörikilta (KIK)",
        "Maanmittarikilta (MK)",
        "Prodeko",
        "Puunjalostajakilta (PJK)",
        "Rakennusinsinöörikilta (IK)",
        "Tietokilta (TiK)",
        "Vuorimieskilta (VK)",
        "Kemistikilta (KK)",
        "Teknologföreningen (TF)",
    ],
    "LUT": [
        "Armatuuri",
        "Cluster",
        "Kaplaaki",
        "Kemiantekniikan kilta (KeTeK)",
        "Koneenrakennuskilta (KRK)",
        "Lateksii",
        "Pelletti",
        "Sätky",
    ],
    "Oulu": [
        "Tuotantotalousteekkarit (OPTIEM)",
        "Arkkitehtikilta",
        "Koneinsinöörikilta (Konekilta)",
        "Prosessikilta",
        "Tietoteekkarit (OTiT)",
        "Ympäristörakentajakilta",
        "Sähköinsinöörikilta (SIK)",
    ],
    "Tampere": [
        "Arkkitehtikilta (TamArk)",
        "Automaatiotekniikan kilta (Autek)",
        "Bioteekkarikilta (Bioner)",
        "Tuotantotalouden kilta Indecs",
        "International Teekkari Guild INTO",
        "Koneenrakentajakilta (KoRK)",
        "Materiaali-insinöörikilta (MIK)",
        "rakentajakilta (TARAKI)",
        "Sähkökilta (Skilta)",
        "Hiukkanen",
        "Tietojohtajakilta (Man@ger)",
        "Tietoteekkarikilta (TiTe)",
        "Urbanum",
        "Ympäristöteekkarikilta (YKI)",
        "Porin teekkarit (PoTka)",
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
