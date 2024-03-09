import asyncio

import aiohttp
import requests
from aiogram import types
from aiogram.types import message
from bs4 import BeautifulSoup

from univer20 import AuthVer2, AuthVer1


async def get_umkd(user, cookies, message: types.Message, user_id):
    url = "https://univer.kstu.kz/student/umkd/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.5",
        "Referer": "http://univer.kstu.kz/student/bachelor/",
        "Upgrade-Insecure-Requests": "1",
    }

    session = requests.session()
    session.cookies.update(cookies)
    response = session.get(url, headers=headers)

    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                disciplines = []
                soup = BeautifulSoup(await response.text(), "html.parser")
                discipline_rows = soup.find_all('tr', class_='link')
                for row in discipline_rows:
                    discipline_name = row.find_all('td')[1].get_text(strip=True)
                    disciplines.append((discipline_name))
                return disciplines
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(message, user_id)
                if cookies is not False:
                    umkd = await get_umkd("user", cookies, message)
                    return umkd

async def Umkd(message: types.Message, user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        umkd = await get_umkd("user", cookies, message, user_id)
        print(umkd)
        return umkd
    else:
        cookies = await AuthVer2.Authorization(message, user_id)
        if cookies is not False:
            umkd = await get_umkd("user", cookies, message, user_id)
            print(umkd)
            return umkd
        else:
            return None  # Возвращаем None в случае неудачной авторизации
