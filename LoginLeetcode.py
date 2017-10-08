# -*- coding: utf-8 -*-
# @Date    : 2017/10/4
# @Author  : hrwhisper

import codecs
import json

import requests
from bs4 import BeautifulSoup


class LoginLeetcode(object):
    """
        用于登录leetcode
    """

    def __init__(self):
        with open('./data/pas') as f:
            res = f.read().splitlines()
        self._username, self._password = res
        self.session = requests.session()
        self.my_head = {
            'Host': 'leetcode.com',
            'Origin': 'https://leetcode.com',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://leetcode.com/accounts/login/',
            'Connection': 'keep-alive',
            'Accept': 'Accept	text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Cache-Control': 'max-age=0'
        }

    def login(self):
        login_url = 'https://leetcode.com/accounts/login/'
        html = self.session.get(login_url, headers=self.my_head).text
        html = BeautifulSoup(html, 'lxml')
        post_data = {
            'csrfmiddlewaretoken': html.find('input', {'name': 'csrfmiddlewaretoken'})['value'],
            'login': self._username,
            'password': self._password
        }
        res = self.session.post(login_url, headers=self.my_head, data=post_data).text
        # print(res)


if __name__ == '__main__':
    s = LoginLeetcode()