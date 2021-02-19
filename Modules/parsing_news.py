# Парсинг новостей с kino.tricolor.tv

import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("..")
import kirptestbot as b

news_number_index = 0

def news_kino_tv():
    global news_text, news_result, news_number_index
    url = 'https://kino.tricolor.tv/news/'
    page = requests.get(url)
    news = []
    first_news = 0
    soup = BeautifulSoup(page.text,'html.parser')
    firstNews = soup.findAll('div', {'class': 'genre-item'})
    first_news_link = "https://kino.tricolor.tv"
    for link in firstNews:
        news.append(first_news_link + link.a.get('href'))
    out_of_range_news = len(news)
    if news_number_index >= first_news and news_number_index < out_of_range_news:
        url_page_news = news[news_number_index]
        news_number_index += 1
        page_news_parsing = requests.get(url_page_news)
        soup2 = BeautifulSoup(page_news_parsing.text,'html.parser')
        news_headline = soup2.find('h1',itemprop="headline")
        news_headline_text = str(news_headline.text)
        news_content = soup2.find('div', {'class': 'content-text'}).findAll('p', limit=2)
        news_text = ''
        news_text_url = '<a href="' + url_page_news + '">Узнать подробности</a>'
        for text in news_content:
            news_text += text.text.strip()
        news_result = '<b>' + news_headline_text +'</b>' + '\n' + news_text + '\n' + news_text_url
    elif news_number_index >= out_of_range_news:
        news_result = "К сожалению, актуальных новостей пока больше нет :("
    return news_result
