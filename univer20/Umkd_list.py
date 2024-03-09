import aiohttp
import requests
from aiogram import types
from bs4 import BeautifulSoup

from univer20 import AuthVer2, AuthVer1


async def get_umkd_download(user, cookies, message: types.Message, user_id, id):
    url = f'https://univer.kstu.kz/student/umkd/{user_id}'
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
                teacher_rows = soup.find_all('tr', class_='brk')
                if teacher_rows:
                    teachers = []  # Список для хранения преподавателей
                    for teacher_row in teacher_rows:
                        teacher_name_element = teacher_row.find('td', class_='ct',
                                                                text=lambda text: 'Преподаватель:' in text)
                        if teacher_name_element:
                            teacher_name = teacher_name_element.get_text(strip=True).replace('Преподаватель:', '')
                            teachers.append(teacher_name)
                        else:
                            print("Преподаватель не найден")
                    if len(teachers) > 0:
                        return teachers  # Возвращаем список преподавателей
                    else:
                        return ['нет данных']  # Возвращаем массив с одним элементом 'нет данных'
                else:
                    return ['нет данных']
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(message, id)
                if cookies is not False:
                    discipline_id = await get_umkd_download("user", cookies, message, user_id, id)
                    return discipline_id
                else:
                    return None


async def Umkd_download(message: types.Message, user_id, id):
    cookies = await AuthVer1.Authorization(id)
    if cookies is not False:
        umkd = await get_umkd_download("user", cookies, message, user_id, id)
        return umkd
    else:
        cookies = await AuthVer2.Authorization(message, user_id)
        if cookies is not False:
            umkd = await get_umkd_download("user", cookies, message, user_id, id)
            return umkd
        else:
            return None  # Возвращаем None в случае неудачной авторизации
