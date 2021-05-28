"""
In this module, we recognize the user's message and respond
"""

from datetime import datetime
from random import choice

import os
import locale
import recognizing
import weather_parser

locale.setlocale(locale.LC_TIME, "ru_RU")


def file_to_list(path):
    """Reads file and converts data to list

    :param path: path to file
    :return: list of rows
    """
    with open(path, 'rt', encoding='utf-8') as data_file:
        return data_file.read().split('\n')


def answer(message: str) -> list:
    """Function for choice the best answer in terms of the prepared phrases

    :param message: user text message
    :return: best answer
    """
    cleaned_message = recognizing.clean(message)

    # At first check for weather forecast request
    acc = [recognizing.similarity(cleaned_message, forecasts[key]["patterns"]) for key in forecasts]
    for key in forecasts:
        if recognizing.similarity(cleaned_message, forecasts[key]["patterns"]) == max(acc) and max(acc) >= 0.58:
            return [forecasts[key]["title"], forecasts[key]["request"]()]

    cleaned_message = recognizing.clean(message, None)
    # At second check in usual phrases
    acc = [recognizing.similarity(cleaned_message, patt) for patt, _ in replicas]
    for patt, resp in replicas:
        if recognizing.similarity(cleaned_message, patt) == max(acc) and max(acc) >= 0.58:
            return [choice(resp)]

    # In the end return message about unsuccessful recognition
    return [choice(unrecognized)]


to_date = lambda x: datetime.fromtimestamp(x).strftime("%A, %d/%m/%Y")
to_time = lambda x: datetime.fromtimestamp(x).strftime("%H:%M:%S")


def current_to_msg(weather: dict) -> str:
    """Converts dict with weather data to pretty message

    :param weather: dict with weather data
    :return: pretty message
    """
    weather = weather["current"]
    message = " "*4 + "{} {} {}\n".format(to_date(weather['dt']).capitalize(), to_time(weather['dt']), weather_emoji[weather["weather"][0]["id"]])
    message += " "*4 + "🌡 {:.01f}℃, ощущается как {:.01f}℃\n".format(weather['temp'], weather['feels_like'])
    message += " "*4 + "🎛 давление {:.01f} мм. рт. ст.\n".format(weather['pressure'] * 0.75)
    message += " "*4 + "💦 влажность {:.0f}%\n".format(weather['humidity'])
    message += " "*4 + "☁ облачность {:.0f}%\n".format(weather['clouds'])
    message += " "*4 + "👁 видимость {:.1f} км.\n".format(weather['visibility'] / 1000)
    message += " "*4 + "💨 скорость ветра {:.01f} м/с\n".format(weather['wind_speed'])
    return message


def hourly_to_msg(weather: dict) -> list:
    """Converts dict with weather data to pretty message

    :param weather: dict with weather data
    :return: pretty message
    """
    messages = ["Сегодня", "Затвра", "Послезавтра"]
    curr_date, current = None, -1

    for item in weather["hourly"]:
        if to_date(item['dt']) != curr_date:
            current += 1
            curr_date = to_date(item['dt'])
            messages[current] += ', ' + curr_date + '\n'

        messages[current] += to_time(item['dt'])[:-3] + ' ' + weather_emoji[item["weather"][0]["id"]] + '\n'
        messages[current] += " " * 4 + "🌡{:>5.01f}℃\n".format(item['temp'])
        messages[current] += " " * 4 + "💨 скорость ветра {:.01f} м/с\n".format(item['wind_speed'])
        messages[current] += " " * 4 + "💦 влажность {:.0f}%\n\n".format(item['humidity'])
    return messages


def weekly_to_msg(weather: dict) -> str:
    """Converts dict with weather data to pretty message

    :param weather: dict with weather data
    :return: pretty message
    """
    message = ""

    for item in weather["daily"]:
        message += to_date(item['dt']).capitalize() + " " + weather_emoji[item["weather"][0]["id"]] + '\n'
        message += " " * 4 + "🌅 утро  {:>6.01f}℃".format(item['temp']['morn']) + '\n'
        message += " " * 4 + "🏞 день  {:>6.01f}℃".format(item['temp']['day']) + '\n'
        message += " " * 4 + "🌇 вечер {:>6.01f}℃".format(item['temp']['eve']) + '\n'
        message += " " * 4 + "🌃 ночь  {:>6.01f}℃".format(item['temp']['night']) + '\n'
        message += " " * 4 + "💨 скорость ветра {:.01f} м/с\n\n".format(item['wind_speed'])
    return message


weather_emoji = {
    500: "🌧",
    501: "🌧",
    502: "🌧",
    503: "🌧",
    504: "🌧",

    800: "☀",
    801: "🌤",
    802: "⛅",
    803: "🌥",
    804: "☁"
}

# for filename in ['after_tomorrow', 'weekly']:
#     with open(f'resources/forecasts/{filename}2.txt', 'wt', encoding='utf-8') as file:
#         data = [recognizing.clean(word, None) for word in file_to_list("resources/forecasts/" + filename + ".txt")]
#         file.write('\n'.join(data))

# with open('resources/replicas/gratitude.txt', 'rt', encoding='utf-8') as file:
#     for word in file.read().split('\n'):
#         print(recognizing.clean(word, None))


forecasts = {
    "current": {
        "patterns": file_to_list("resources/forecasts/current2.txt"),
        "title": "Текущее состояние погоды",
        "request": lambda: current_to_msg(weather_parser.get_weather(weather_parser.CURRENT))
    },
    "today": {
        "patterns": file_to_list("resources/forecasts/today2.txt"),
        "title": "Погода сегодня",
        "request": lambda: hourly_to_msg(weather_parser.get_weather(weather_parser.HOURLY))[0]
    },
    "tomorrow": {
        "patterns": file_to_list("resources/forecasts/tomorrow2.txt"),
        "title": "Погода завтра",
        "request": lambda: hourly_to_msg(weather_parser.get_weather(weather_parser.HOURLY))[1]
    },
    "after_tomorrow": {
        "patterns": file_to_list("resources/forecasts/after_tomorrow2.txt"),
        "title": "Погода послезавтра",
        "request": lambda: hourly_to_msg(weather_parser.get_weather(weather_parser.HOURLY))[2]
    },
    "weekly": {
        "patterns": file_to_list("resources/forecasts/weekly2.txt"),
        "title": "8-дневный прогноз погоды",
        "request": lambda: weekly_to_msg(weather_parser.get_weather(weather_parser.WEEKLY))
    }
}

replicas = []
for file in os.listdir("resources/replicas"):
    if file.startswith('answer_'):
        data = file_to_list("resources/replicas/" + file[7:])
        ans = file_to_list("resources/replicas/" + file)
        replicas.append((data, ans))

unrecognized = file_to_list('resources/Unrecognized.txt')
print(replicas)
