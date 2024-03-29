# Скраппер новостей с сайта Забгу

## Описание
Этот проект представляет собой простой скраппер новостей с сайта ЗабГУ. Он извлекает данные о новостях, включая заголовок, дату, теги и текст новости.

## Установка
Для работы с этим проектом вам потребуется Python 3.7 или выше. Вы также должны установить следующие библиотеки:
- pandas
- requests
- beautifulsoup4

Вы можете установить их с помощью pip:
```bash
pip install pandas requests beautifulsoup4
```

## Запуск

Чтобы запустить скраппер, просто запустите файл main.py с помощью Python:
```bash
python main.py
```
По умолчанию парсер будет извлекать новости с первых 50 страниц. Вы можете изменить это, изменив аргумент функции news_scrapper в конце файла.

## Результат
После выполнения скраппера данные будут сохранены в файле zabgu_data.csv в формате CSV. 
Каждая строка в файле представляет собой одну новость, а столбцы содержат заголовок, дату, теги и текст новости.