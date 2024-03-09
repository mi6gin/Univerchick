import asyncio
import os
from urllib.parse import urlparse

import aiohttp
import requests
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import message, URLInputFile, BufferedInputFile
from bs4 import BeautifulSoup

from settings import bot
from univer20 import AuthVer2, AuthVer1


async def get_umkd_get_name(user, cookies, message: types.Message, user_id, id, num, state: FSMContext):
    print(id)
    url = f'https://univer.kstu.kz/student/umkd/{num}'
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

                soup = BeautifulSoup(await response.text(), "html.parser")
                files = []
                file_rows = soup.find_all('tr', class_='file')
                desired_id = id
                for row in file_rows:
                    file_id = int(row.get('id'))
                    print(1909090990)
                    print(id)
                    print(2121212121)
                    print(file_id)
                    if file_id == desired_id:
                        file_name = row.find('td', style='overflow: hidden').find('a').get_text(strip=True)
                        files.append({"name": file_name})  # Добавляем id и имя файла в виде словаря
                        for file in files:
                            name = file['name']
                            await get_umkd_download_file("user", cookies, message, user_id, id, num, name, state)
            else:
                print("Ошибка при получении списка файлов")
                cookies = await AuthVer2.Authorization(message, user_id)
                if cookies is not False:
                    umkd = await get_umkd_get_name("user", cookies, message, user_id, id, num)
                    return umkd

async def get_umkd_download_file(user, cookies, message: types.Message, user_id, id, num, name, state: FSMContext):
    print(id)
    url = f'https://univer.kstu.kz/student/umkd/get/{id}/{num}'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.5",
        "Referer": "http://univer.kstu.kz/student/bachelor/",
        "Upgrade-Insecure-Requests": "1",
    }

    session = requests.session()
    session.cookies.update(cookies)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await state.get_data()
                message_to_delete = data.get('message_to_delete')
                await message_to_delete.delete()
                content = await response.read()
                file = BufferedInputFile(content, filename=name)
                await bot.send_document(user_id, file)

                print(f"Файл {name} успешно отправлен в Telegram.")
            else:
                print("Ошибка при получении списка файлов")
                cookies = await AuthVer2.Authorization(message, user_id)
                if cookies is not False:
                    umkd = await get_umkd_download_file("user", cookies, message, user_id, id, num)
                    return umkd

async def Umkd_download(message: types.Message, user_id, id, num, state: FSMContext):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        umkd = await get_umkd_get_name("user", cookies, message, user_id, id, num, state)
        print(umkd)
        return umkd
    else:
        cookies = await AuthVer2.Authorization(message, user_id)
        if cookies is not False:
            umkd = await get_umkd_get_name("user", cookies, message, user_id, id, num, state)
            print(umkd)
            return umkd
        else:
            return None  # Возвращаем None в случае неудачной авторизации
