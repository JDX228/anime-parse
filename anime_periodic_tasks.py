import requests
import re

from bs4 import BeautifulSoup


import asyncio
import httpx


list_anime = [
    "Семья шпиона",
    "Мир отомэ-игр — это тяжёлый мир для мобов",
    "Госпожа Кагуя: в любви как на войне",
    "Рыцарь-скелет вступает в параллельный мир",
    "Восхождение героя щита 2 сезон",
    "Перестану быть героем",
    "Тусовщик Кунмин",
    "Величайший Повелитель Демонов перерождается как типичное ничтожество",
]

link = "https://naruto-base.su/novosti/drugoe_anime_ru"
url_base = "https://naruto-base.su/"
# Количество страниц, которое будет просматривать код
pages = 3



async def get_anime(client, url):
        response = await client.get(url)
        return response.text


async def main():

    async with httpx.AsyncClient() as client:
        anime_list_parse_html = []
        tasks = []
        for number in range(1, pages):
            url = f'{link}?page{number}'
            tasks.append(asyncio.ensure_future(get_anime(client, url)))

        animes = await asyncio.gather(*tasks)
        # Митиситу кажется что тут можно забабахать async for
        for anime in animes:
            anime_list_parse_html.append(anime)
        return anime_list_parse_html
    

site = ''.join(asyncio.run(main()))
soup = BeautifulSoup(site, "lxml")
tag_h2 = soup.find_all('h2')

print(tag_h2)

#for ak in site:
#    k = BeautifulSoup(ak, "lxml")
#    for b in k.find_all('h2'):
#        for a in list_anime:
#            if a in b.get_text():
#                print(b)
#            continue
## Функция возвращающая ссылку на последнюю серию аниме по названию в заголовке файла, заданному в параметрах
#def data_last_element_anime(id=None):
#    for i in range(pages):
#        anime_ID = [
#            link["href"]
#            for link in (data_scrapping(url + "?page" + str(i + 1), "a"))
#            if id in link.get_text()
#        ]
#        if len(anime_ID) == 0:
#            pass
#        else:
#            link_anime = url_base + anime_ID[0]
#            # Поиск ссылки на последний эпизод аниме с сабами и без на портале Sibnet
#            last_episode_sub = data_scrapping(link_anime, "a", id="ep6")
#            # last_episode = data_scrapping(link_anime, 'a', id="ep14")
#            # result_sub = re.search(r'\d{7}', str(last_episode_sub))[0]
#            try:
#                result_dub = re.search(r"\d{7}", str(last_episode_sub))[0]
#            except TypeError:
#                pass
#            else:
#                link_name_and_element_anime = data_scrapping(link_anime, "h1")[0].text
#                # link_result_sub = 'https://video.sibnet.ru/shell.php?videoid=' + result_sub
#                link_result_dub = (
#                    "https://video.sibnet.ru/shell.php?videoid=" + result_dub
#                )
#                try:
#                    anime_title_anime = Anime.objects.create(
#                        title_anime=link_name_and_element_anime,
#                        link_anime=link_result_dub,
#                    )
#                except IntegrityError:
#                    pass
#                else:
#                    anime_title_anime.save(force_update=True)
#                # puk[link_name_and_element_anime] = link_result_dub
#                break
#
#
#def last_series_anime():
#    logging.warning("It is time to start the dramatiq task anime")
#    for anime in list_anime:
#        data_last_element_anime(id=anime)
