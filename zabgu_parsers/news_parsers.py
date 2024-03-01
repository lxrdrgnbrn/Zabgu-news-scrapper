# Импортируем необходимые библиотеки
import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL-адрес, с которого мы будем извлекать новости
url = 'https://zabgu.ru/php/news.php?'


def get_news_text(link):
    """
    Функция для получения текста новости по ссылке.

    Параметры:
    link (str): Ссылка на новость.

    Возвращает:
    text (list): Список абзацев текста новости.
    """
    # Получаем ссылку на полную новость
    news_link = 'https://zabgu.ru' + link
    # Делаем запрос на страницу новости
    with requests.get(news_link) as news_response:
        news_page = BeautifulSoup(news_response.text, 'lxml')
        # Извлекаем текст новости
        news_div = news_page.find('div', {'id': 'full_text'})
        p_tags = news_div.findAll('p')
        text = [p.text for p in p_tags]
    return text


def get_news_data(page_number, data_frame):
    """
    Функция для получения данных новостей с определенной страницы.

    Параметры:
    page_number (int): Номер страницы для извлечения новостей.
    data_frame (DataFrame): DataFrame для добавления новых данных.

    Возвращает:
    data_frame (DataFrame): Обновленный DataFrame с новыми данными.
    """
    # Делаем запрос на страницу новостей
    with requests.get(url + str(page_number)) as response:
        page_raw = BeautifulSoup(response.text, 'lxml')

    # Извлекаем превью новостей
    news_preview = page_raw.find_all('div', {'class': 'preview_new'})
    news_preview_end = page_raw.find_all('div', {'class': 'preview_new_end'})

    # Обрабатываем каждую новость
    for news in news_preview + news_preview_end:
        # Извлекаем данные новости
        header = news.find('div', {'class': 'headline'}).text
        year = news.find('p', {'class': 'yearInTileNewsOnPageWithAllNews'}).text
        day_month = news.find('p', {'class': 'day'}).text
        date = day_month[0:-3] + ' ' + day_month[-3:] + ' ' + year
        tags_raw = news.find('div', {'class': 'markersContainer'}).find_all('a', {'class': 'marker_news'})
        tags = [tag.text for tag in tags_raw]
        news_text = get_news_text(news.find('a')['href'])

        # Добавляем данные новости в DataFrame
        data_frame._append(
            {'Header': header, 'Date': date, 'Tags': tags, 'Text': news_text},
            ignore_index=True)

    return data_frame


def news_scrapper(page_count: int):
    """
    Функция для скраппинга новостей с заданного количества страниц.

    Параметры:
    page_count (int): Количество страниц для скраппинга.

    Возвращает:
    data_frame (DataFrame): DataFrame с данными новостей.
    """
    # Создаем пустой DataFrame
    data_frame = pd.DataFrame()

    # Обрабатываем каждую страницу
    for page_number in range(1, page_count + 1):
        try:
            # Получаем данные новостей с текущей страницы
            data_frame = get_news_data(page_number, data_frame)
        except Exception as e:
            print(f"Произошла ошибка на странице {page_number}: {e}")
    return data_frame
