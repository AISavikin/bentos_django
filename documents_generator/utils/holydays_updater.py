import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
from ..config import *

filename = PATH_TO_JSON_HOLIDAYS

def fetch_holidays(year):
    """
    Получает данные о выходных днях за указанный год с API isdayoff.ru.

    :param year: Год, за который нужно получить данные.
    :return: Список, где 1 — выходной, 0 — рабочий день.
    :raises Exception: Если запрос к API завершился ошибкой.
    """
    url = f"https://isdayoff.ru/api/getdata?year={year}&delimeter=."
    response = requests.get(url)
    if response.status_code == 200:
        return list(map(int, response.text.split('.')))
    else:
        raise Exception(f"Ошибка при запросе данных: {response.status_code}")


def save_holidays_to_json(year, holidays, filename=filename):
    """
    Сохраняет данные о выходных днях в JSON-файл.

    :param year: Год, для которого сохраняются данные.
    :param holidays: Список выходных дней.
    :param filename: Имя файла для сохранения (по умолчанию filename).
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[str(year)] = holidays  # Год сохраняем как строку для совместимости с JSON.

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_holidays_from_json(filename=filename):
    """
    Загружает данные о выходных днях из JSON-файла.

    :param filename: Имя файла для загрузки (по умолчанию filename).
    :return: Словарь с данными о выходных днях, где ключ — год (строка), значение — список выходных дней.
    """
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def get_weekends(start_date: datetime, days: int) -> list[datetime]:
    """Возвращает список выходных дней в указанном диапазоне"""
    holidays = load_holidays_from_json()
    weekends = []
    current_day = start_date

    for _ in range(days):
        year = str(current_day.year)
        day_of_year = current_day.timetuple().tm_yday - 1

        if holidays.get(year) and len(holidays[year]) > day_of_year:
            if holidays[year][day_of_year] == 1:
                weekends.append(current_day)

        current_day += timedelta(days=1)

    return weekends

def is_work_day(check_date: datetime, holidays: dict):
    day_of_year = check_date.timetuple().tm_yday - 1
    holiday =  holidays.get(str(check_date.year))[day_of_year]
    return True if holiday == 0 else False

if __name__ == '__main__':
    year = 2025
    holidays = fetch_holidays(year)
    save_holidays_to_json(year, holidays)