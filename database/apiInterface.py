import requests


def putItem(year, guild, campus, score):
    # post to https://wappufiilisweb.vercel.app/api/fiilis
    data = {
        "year": year,
        "guild": guild,
        "campus": campus,
        "score": score,
    }
    response = requests.post("https://wappufiilisweb.vercel.app/api/fiilis", json=data)
    print(response.status_code)
    print(response.text)
    return response.status_code
