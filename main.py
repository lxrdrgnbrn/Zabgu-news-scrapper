from zabgu_parsers.news_parsers import news_scrapper

# Имя файла для сохранения данных
file_name = 'zabgu_data.csv'
# Парсим новости с 10 страниц и сохраняем данные в файл
news_scrapper(50).to_csv(file_name, sep='\t', encoding='utf-16')
