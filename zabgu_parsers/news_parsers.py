# Импортируем необходимые библиотеки
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup

# URL-адрес, с которого мы будем извлекать новости
url = 'https://zabgu.ru/php/news.php?category=1&page='
file_path = os.path.join(os.getcwd(), 'data')
file_path_img = os.path.join(file_path, 'images')


def create_directory(directory_path):
    """
    Создает директорию, если она не существует.

    Аргументы:
    directory_path (str): Путь к директории, которую нужно создать.

    Возвращает:
    None
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def download_image(image_url, path):
    """
    Функция для скачивания изображения по URL.

    Параметры:
    image_url (str): URL изображения.
    path (str): Путь к файлу, в который будет сохранено изображение.
    """
    image_url = 'https://zabgu.ru' + image_url
    # Делаем запрос на скачивание изображения
    response = requests.get(image_url)

    # Проверяем, что запрос был успешным
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
            file.close()


def get_news_text(link, img_name):
    """
    Функция для получения текста новости по ссылке.

    Параметры:
    link (str): Ссылка на новость.
    index (int): Индекс новости.

    Возвращает:
    text (list): Список абзацев текста новости.
    """
    # Получаем ссылку на полную новость
    news_link = 'https://zabgu.ru' + link
    # Делаем запрос на страницу новости
    with requests.get(news_link) as news_response:
        news_page = BeautifulSoup(news_response.text, 'lxml')
        # Извлекаем данные новости
        header = news_page.find('div', {'id': 'full_text'}).h2.span.strong.text
        header = header.replace('\xa0', ' ').replace('\n', ' ')
        year = news_page.find('p', {'class': 'year'}).text
        day_month = news_page.find('p', {'class': 'day'}).text
        date = day_month[0:-3] + ' ' + day_month[-3:] + ' ' + year
        tags_raw = news_page.find(
            'div',
            {'class': 'markersContainer openNewsMarkersContainer'}).find_all(
            'a',
            {'class': 'marker'})
        tags = [tag.text for tag in tags_raw]
        news_div = news_page.find('div', {'id': 'full_text'})
        p_tags = news_div.findAll('p')
        text = [p.text.replace('\xa0', ' ').replace('\n', ' ') for p in p_tags if
                'day' not in p.get('class', []) and 'year' not in p.get('class', [])]
        # Извлекаем URL изображения
        image_url = news_div.find('img')['src'] if news_page.find('img') else None
        if image_url:
            # Скачиваем изображение
            download_image(image_url, os.path.join(file_path_img, img_name))
        news_df = pd.DataFrame([{'Header': header, 'Date': date, 'Tags': ', '.join(tags),
                                 'Text': ' '.join(text).strip(), 'Image': img_name}])
    return news_df


def get_news_data(page_number):
    """
    Функция для получения данных новостей с определенной страницы.

    Параметры:
    page_number (int): Номер страницы для извлечения новостей.

    Возвращает:
    data_frames (list): Список DataFrame с данными новостей.
    """
    data_frames = []
    # Делаем запрос на страницу новостей
    with requests.get(url + str(page_number)) as response:
        page_raw = BeautifulSoup(response.text, 'lxml')

    # Извлекаем превью новостей
    news_preview = page_raw.find_all('div', {'class': 'preview_new'})
    news_preview_end = page_raw.find_all('div', {'class': 'preview_new_end'})
    # Обрабатываем каждую новость
    for index, news in enumerate(news_preview + news_preview_end):
        # Создаем новый DataFrame для новости и добавляем его в список
        img_name = 'image_'+str(page_number)+'_'+str(index)+'.jpg'
        news_df = pd.DataFrame(get_news_text(news.find('a')['href'], img_name))
        data_frames.append(news_df)

    return data_frames


def scrape_news(page_count: int):
    """
    Функция для скраппинга новостей с заданного количества страниц.

    Параметры:
    page_count (int): Количество страниц для скраппинга.

    Возвращает:
    data_frame (DataFrame): DataFrame с данными новостей.
    """
    # Создаем пустой список для DataFrame'ов
    data_frames = []

    # Обрабатываем каждую страницу
    for page_number in range(1, page_count + 1):
        try:
            # Получаем данные новостей с текущей страницы
            page_data_frames = get_news_data(page_number)
            data_frames.extend(page_data_frames)
        except Exception as e:
            print(f"Произошла ошибка на странице {page_number}: {e}")

    # Объединяем все DataFrame'ы в один
    data_frame = pd.concat(data_frames, ignore_index=True)

    return data_frame


def save_data(data_frame, path):
    """
    Функция для сохранения DataFrame в CSV-файл.

    Параметры:
    data_frame (DataFrame): DataFrame, который нужно сохранить.
    path (str): Путь к файлу, в который будут сохранены данные.
    """
    data_frame.to_csv(os.path.join(path, f'data.csv'), sep=',', encoding='utf-16')


def parse(page_count: int):
    """
    Функция для парсинга новостей и сохранения полученных данных.

    Аргументы:
    page_count (int): Количество страниц для парсинга.

    Возвращает:
    None. Выводит сообщение 'Success!' в случае успешного выполнения.

    Примечания:
    - Функция использует другую функцию `scrape_news` для извлечения данных с указанного количества страниц.
    - Полученные данные сохраняются с помощью функции `save_data`.
    - Путь к файлу для сохранения данных должен быть определен в переменной `file_path`.
    """
    create_directory(file_path_img)
    create_directory(file_path)
    save_data(scrape_news(page_count), file_path)
    return print('Success!')
