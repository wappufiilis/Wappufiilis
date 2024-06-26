import base64
import hashlib
import json
from enum import Enum


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def userToCallbackData(user: dict):
    dataString = (
        f"campus::{user['campus']}::guild::{user['guild']}::year::{user['year']}"
    )
    return json.dumps(user)


import base64
import gzip
import json


def compressCallBackData(data: dict):
    csv = ""
    for i in range(1 + max(int(number.value) for number in KeyboardKeys)):
        if str(i) in data:
            csv += str(data[str(i)]) + ","
        else:
            csv += ","
    csv = csv[:-1]
    csv_str = csv.encode("utf-8")
    compressed = gzip.compress(csv_str)
    encoded = base64.b64encode(compressed).decode("utf-8")
    # print(data, "Compressed data: ", encoded)
    # Long names are too long. figure how to compress more.
    return encoded


def decompressCallBackData(data: str):
    decoded = base64.b64decode(data.encode("utf-8"))
    decompressed = gzip.decompress(decoded)
    csv = decompressed.decode("utf-8")
    items = csv.split(",")
    data = {}
    for i, item in enumerate(items):
        if item:
            data[str(i)] = item
    return data


class DatabaseKeys(Enum):
    USER_ID = "user_id"
    GUILD = "guild"
    CAMPUS = "campus"
    YEAR = "study_year"
    TIMESTAMP = "timestamp"
    LAST_SCORE = "last_score"
    SCORES = "scores"


class KeyboardKeys(Enum):
    USER_ID = "1"
    GUILD = "2"
    CAMPUS = "3"
    YEAR = "4"
    SCORE = "5"
    TIMESTAMP = "6"
    NEW_SCORE = "7"
    MENU = "8"
    PAGINATION = "9"


class MenuKeys(Enum):
    CAMPUS = "1"
    GUILD = "2"
    YEAR = "3"
    RESULTS = "4"
    PERSONAL_INFO = "5"
    SCORE = "6"
    GRAPH = "7"
    GRAPH_CAMPUS = "8"
    GRAPH_GUILD = "9"
    GRAPH_YEAR = "10"
    GRAPH_USER = "11"


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


class Kampus(Enum):
    AALTO = "1"
    LUT = "2"
    OULU = "3"
    TAMPERE = "4"
    TURKU = "5"
    VAASA = "6"
    JYVÄSKYLÄ = "7"
    OTHER = "99"
    NONE = "None"


Killat = {
    Kampus.AALTO.value: [
        "AK",
        "AS",
        "Athene",
        "CRUST",
        "DaDa",
        "DG",
        "FK",
        "GRRR",
        "IK",
        "Inkubio",
        "KIK",
        "KK",
        "Klaffi",
        "Klubi",
        "KOOMA",
        "KY",
        "MK",
        "NuDe",
        "PJK",
        "Prodeko",
        "PT",
        "SIK",
        "SISTA",
        "TF",
        "TiK",
        "TOKYO",
        "VISTA",
        "VK",
    ],
    Kampus.LUT.value: [
        "Armatuuri",
        "Cluster",
        "Kaplaaki",
        "KeTeK",
        "KRK",
        "Lateksii",
        "Pelletti",
        "Sätky",
    ],
    Kampus.OULU.value: [
        "AK",
        "Kone",
        "OPTIEM",
        "OTiT",
        "Prose",
        "SIK",
        "YRK",
        "OLTO",
    ],
    Kampus.TAMPERE.value: [
        "TamArk",
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
    Kampus.TURKU.value: [
        "Adamas",
        "Asklepio",
        "DaTe",
        "Digit",
        "Machina",
        "Nucleus",
        "Kemistklubben",
    ],
    Kampus.VAASA.value: ["Tutti ry"],
    Kampus.JYVÄSKYLÄ.value: [
        "Algo",
    ],
    Kampus.OTHER.value: [
        "Other",
    ],
}


def dropFromCallbackData(data: dict, key: str):
    if key in data:
        del data[key]
    return data
