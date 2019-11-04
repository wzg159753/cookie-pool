# -*-coding:utf-8 -*-


import requests


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/67.0.3396.99 Safari/537.36'}


def get_page(url):
    """获取一个网页"""
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.content
    except:
        return None

