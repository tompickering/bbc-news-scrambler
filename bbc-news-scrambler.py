#!/usr/bin/env python3

# pip3 install bbc-news

import bbc
import sys
import random


def scramble(articles):
    n_articles = len(articles)

    if n_articles < 2:
        sys.exit(1)

    i0 = random.randrange(n_articles)
    i1 = i0

    while i1 == i0:
        i1 = random.randrange(n_articles)

    a0 = articles[i0]
    a1 = articles[i1]

    title = a0['title']
    image = a1['image_link']

    a0_n = a0['news_link']
    a1_n = a1['news_link']

    print(title)
    print(image)


if __name__ == '__main__':
    news = bbc.news.get_news(bbc.Languages.English)

    categories = news.news_categories()

    articles = []

    for cat in categories:
        articles += news.news_category(cat)

    articles = [a for a in articles if a['title'] and a['image_link']]

    while True:
        try:
            scramble(articles)
            input()
        except KeyboardInterrupt:
            break
