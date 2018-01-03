# -*- coding: utf-8 -*-
# @Date    : 2017/10/4
# @Author  : hrwhisper


import requests
from bs4 import BeautifulSoup


class LoginLeetcode(object):
    """
        用于登录leetcode
    """
    my_head = {
        'Host': 'leetcode.com',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://leetcode.com/',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Cache-Control': 'max-age=0'
    }

    def __init__(self):
        with open('./data/pas') as f:
            res = f.read().splitlines()
        self._username, self._password = res
        self.session = requests.session()

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


if __name__ == '__main__':
    s = LoginLeetcode()
    s.login()


