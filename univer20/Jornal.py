import asyncio

import aiohttp
import requests
from aiogram import types
from aiogram.types import message
from bs4 import BeautifulSoup

from univer20 import AuthVer2, AuthVer1


async def get_jornal(user, cookies, message: types.Message, user_id):
    url = "http://univer.kstu.kz/student/attendance/full/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.5",
        "Referer": "http://univer.kstu.kz/student/bachelor/",
        "Upgrade-Insecure-Requests": "1",
    }

    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                schedule_data = {}
                soup = BeautifulSoup(await response.text(), "html.parser")
                subject_elements = soup.find_all("td", class_="ct",
                                                 unselectable="on")  # Находим все элементы с названием предметов

                for subject_element in subject_elements:
                    subject = subject_element.get_text(strip=True).split("[")[0].strip()  # Извлекаем название предмета
                    if subject.endswith("("):
                        subject = subject[:-1]
                    scores_element = subject_element.find_next("td", class_="ct")  # Находим элемент с баллами предмета
                    scores_text = scores_element.get_text(strip=True)  # Получаем текст с баллами

                    # Извлекаем баллы РК1
                    rk1_score = ""
                    rk1_index = scores_text.find("РК1 (100):")
                    if rk1_index != -1:
                        rk1_score = scores_text[rk1_index + len("РК1 (100):"):].split()[0].strip()

                    # Извлекаем баллы РК2, начиная поиск с позиции, где начинается РК2
                    rk2_score = ""
                    rk2_index = scores_text.find("РК2 (100):")
                    if rk2_index != -1:
                        rk2_score = scores_text[rk2_index + len("РК2 (100):"):].split()[0].strip()

                    if rk1_score.endswith("РК2"):
                        rk1_score = rk1_score[:-3]
                    # Добавляем данные в расписание
                    schedule_data[subject] = {
                        "RK1": rk1_score,
                        "RK2": rk2_score
                    }

                return schedule_data
            else:
                print("Ошибка получения информации о журнале")
                cookies = await AuthVer2.Authorization(message, user_id)
                if cookies is not False:
                    schedule = await get_jornal("user", cookies, message)
                    return schedule

async def Jornal(message: types.Message, user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        schedule = await get_jornal("user", cookies, message, user_id)
        print(schedule)
        return schedule
    else:
        cookies = await AuthVer2.Authorization(message, user_id)
        if cookies is not False:
            schedule = await get_jornal("user", cookies, message, user_id)
            print(schedule)
            return schedule
        else:
            return False
