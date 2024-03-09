import aiohttp
from bs4 import BeautifulSoup
from aiogram import types
from univer20 import AuthVer2, AuthVer1


async def get_user_info(user, cookies, message: types.Message, user_id):
    url = "http://univer.kstu.kz/student/bachelor/"
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
                soup = BeautifulSoup(await response.text(), "html.parser")
                name_element = soup.find("div", class_="links")
                inner_div = soup.find("div", class_="inner")

                # Находим все теги <td> внутри этого <div>
                td_elements = inner_div.find_all("td")

                name = ' '.join(name_element.text.strip().split()[:2])
                form_education = td_elements[1].text.strip()
                level_education = td_elements[3].text.strip()
                department = td_elements[5].text.strip()
                category_education = td_elements[7].text.strip()
                faculty = td_elements[9].text.strip()
                special = td_elements[11].text.strip()
                course = td_elements[13].text.strip()
                print("ФИО:", name)
                std_data = {
                    "name": name,
                    "form_education": form_education,
                    "level_education": level_education,
                    "department": department,
                    "category_education": category_education,
                    "faculty": faculty,
                    "special": special,
                    "course": course,
                }
                return std_data
            else:
                print("Ошибка получения информации о пользователе")
                cookies = await AuthVer2.Authorization(message, user_id)
                if cookies is not False:
                    user = await get_user_info("user", cookies, message, user_id)
                    return user
                    print(schedule)

async def Username(message: types.Message, user_id):
    cookies = await AuthVer1.Authorization(user_id)
    if cookies is not False:
        std_data = await get_user_info("user", cookies, message, user_id)
        return std_data
    else:
        cookies = await AuthVer2.Authorization(message, user_id)
        if cookies is not False:
            std_data = await get_user_info("user", cookies, message, user_id)
            return std_data
        else:
            return None  # Возвращаем None в случае неудачной авторизации