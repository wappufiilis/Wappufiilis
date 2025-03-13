from enum import Enum
from typing import Dict, List

class Campus(str, Enum):
    TAMPERE = "tampere"
    HELSINKI = "helsinki"
    OULU = "oulu"
    TURKU = "turku"
    JYVASKYLA = "jyvaskyla"
    LAPPEENRANTA = "lappeenranta"
    VAASA = "vaasa"
    KUOPIO = "kuopio"
    ROVANIEMI = "rovaniemi"

class MenuKey(str, Enum):
    CAMPUS = "campus"
    GUILD = "guild"
    YEAR = "year"
    RESULTS = "results"
    PERSONAL_INFO = "personal_info"
    SCORE = "score"
    GRAPH = "graph"
    GRAPH_CAMPUS = "graph_campus"
    GRAPH_GUILD = "graph_guild"
    GRAPH_YEAR = "graph_year"
    GRAPH_USER = "graph_user"

class KeyboardKey(str, Enum):
    GUILD = "guild"
    CAMPUS = "campus"
    YEAR = "year"
    SCORE = "score"
    TIMESTAMP = "timestamp"
    NEW_SCORE = "new_score"
    MENU = "menu"
    PAGINATION = "pagination"

# Guild mappings for each campus
GUILDS: Dict[Campus, List[str]] = {
    Campus.TAMPERE: ["TiK", "TeK", "TARAKI", "TREY", "Tamy", "TYY", "TKO-äly"],
    Campus.HELSINKI: ["Athene", "Kylteri", "Murska", "NYYT", "OTiT", "Prodeko"],
    # Add other campuses as needed
}

# Year options
YEARS = ["2020", "2021", "2022", "2023", "2024"]

# UI Constants
ITEMS_PER_PAGE = 9 