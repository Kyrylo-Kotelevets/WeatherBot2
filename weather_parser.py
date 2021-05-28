"""This module contains sources and functions for downloading weather data"""

import json
import requests

SOURCE = "http://api.openweathermap.org/data/2.5/"
API_KEY = "1bf25d670cd1c0392a2c8be563e7391d"

CURRENT = SOURCE + "onecall?lat=50&lon=36.25&exclude=minutely,hourly,daily,alerts&units=metric&appid={}" .format(API_KEY)
HOURLY = SOURCE + "onecall?lat=50&lon=36.25&exclude=current,minutely,daily,alerts&units=metric&appid={}" .format(API_KEY)
WEEKLY = SOURCE + "onecall?lat=50&lon=36.25&exclude=current,minutely,hourly,alerts&units=metric&appid={}" .format(API_KEY)
ALL_DATA = SOURCE + "onecall?lat=50&lon=36.25&units=metric&appid={}" .format(API_KEY)


def get_weather(source_url: str) -> dict:
    """This functions parses data from given source

    :param source_url: url with weather data in json format
    :return: dict with weather data
    """
    response = requests.get(source_url)

    if response:
        parsed = response.content
        data = json.loads(parsed)
        return data
    raise Exception("Не удалось загузить данные по адресу %s" % source_url)
