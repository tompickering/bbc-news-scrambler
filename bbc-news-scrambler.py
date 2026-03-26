#!/usr/bin/env python3

# pip3 install bbc-news

import bbc
import sys
import random
import requests
import webbrowser
import tkinter as tk

from io import BytesIO
from PIL import Image, ImageTk


WIDTH = 600
LMB = '<Button-1>'


def scramble(root, articles):
    global WIDTH

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
    image_link = a1['image_link']

    image_response = requests.get(image_link)
    image_data = BytesIO(image_response.content)
    image = Image.open(image_data)
    img_sc = WIDTH / image.width
    image = image.resize((int(image.width*img_sc), int(image.height*img_sc)))


    if image_response.status_code != 200:
        return False

    if image_response.headers.get('content-type') != 'image/webp':
        return False

    image_tk = ImageTk.PhotoImage(image)

    image_label = tk.Label(root, image=image_tk)
    image_label.image = image_tk
    image_label.pack()

    headline_label = tk.Label(root, text=title)
    headline_label.pack()

    redo_label = tk.Label(root, text='RESCRAMBLE')
    redo_label.pack()

    a0_n = a0['news_link']
    a1_n = a1['news_link']

    image_label.bind(LMB, lambda _: webbrowser.open(a1_n))
    headline_label.bind(LMB, lambda _: webbrowser.open(a0_n))

    def redo():
        redo_label.destroy()
        headline_label.destroy()
        image_label.destroy()
        scramble(root, articles)

    redo_label.bind(LMB, lambda _: redo())

    return True


if __name__ == '__main__':
    root = tk.Tk()
    root.title('BBC News Scrambler')

    news = bbc.news.get_news(bbc.Languages.English)

    categories = news.news_categories()

    links = set()
    articles = []

    for cat in categories:
        for article in news.news_category(cat):
            if not (article['title'] and article['image_link']):
                continue

            if article['news_link'] in links:
                continue

            links.add(article['news_link'])
            articles.append(article)

    scramble(root, articles)

    root.mainloop()
