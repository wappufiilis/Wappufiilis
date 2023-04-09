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
    print("data string is", dataString)
    return json.dumps(user)


import base64
import gzip
import json


def compressCallBackData(data: dict):
    # data to csv string
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
    # print(data, "encoded is", encoded, len(encoded), "decoded is", decompressCallBackData(encoded))
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


class KeyboardKeys(Enum):
    USER_ID = "1"
    GUILD = "2"
    CAMPUS = "3"
    YEAR = "4"
    SCORE = "5"
    TIMESTAMP = "6"
    NEW_SCORE = "7"
    MENU = "8"


class MenuKeys(Enum):
    CAMPUS = "1"
    GUILD = "2"
    YEAR = "3"


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


Killat = {
    Kampus.AALTO.value: [
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
        "OPTIEM",
        "Arkkitehtikilta",
        "Konekilta",
        "Prosessikilta",
        "OTiT",
        "Ympäristörakentajakilta",
        "SIK",
    ],
    Kampus.TAMPERE.value: [
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
    Kampus.TURKU.value: [
        "Adamas",
        "Asklepio",
        "Digit",
        "Machina",
        "Nucleus",
        "Kemistklubben",
        "DaTe",
    ],
    Kampus.VAASA.value: ["Tutti ry"],
    Kampus.JYVÄSKYLÄ.value: [
        "Algo",
    ],
}


def dropFromCallbackData(data: dict, key: str):
    if key in data:
        del data[key]
    return data
