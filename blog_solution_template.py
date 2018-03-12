# -*- coding: utf-8 -*-
# @Date    : 2017/10/8
# @Author  : hrwhisper
import codecs

import requests
from bs4 import BeautifulSoup

from LeetcodeProblemList import LeetcodeProblemList


def get_description(base_url):
    url = base_url + 'description/'
    print(url)
    html = requests.get(url, headers=LeetcodeProblemList.my_head).text
    soup = BeautifulSoup(html, "lxml")
    return soup.find('meta', {'name': 'description'})['content']


def main(id_list, update_from_leetcode=False):
    id_list.sort()
    leetcode_list = LeetcodeProblemList().get_list(update_from_leetcode=update_from_leetcode)
    with codecs.open('./data/current_solution.html', 'w', 'utf-8') as f:
        titles = [(leetcode_list[_id].number, leetcode_list[_id].title) for _id in id_list]
        f.write('本次题解包括\n<ul>\n')
        for t in titles:
            f.write('<li><strong>{}</strong>. {}</li>\n'.format(t[0], t[1]))
        f.write('</ul>\n<!--more-->\n')

        ans = []
        for i, _id in enumerate(id_list):
            cur_problem = leetcode_list[_id]
            print(cur_problem)
            ans.append('\n<br>\n<br><hr>\n<br>\n<br>\n')
            ans.append('<h3>{}. {}</h3>\n\n'.format(int(cur_problem.number), cur_problem.title))
            ans.append('<blockquote>{}</blockquote>'.format(get_description(cur_problem.url)))
            ans.append('题目地址：<a href="{}" target="_blank" rel="nofollow">leetcode {}</a>\n' \
                       .format(cur_problem.url, cur_problem.title))
            ans.append('题目大意：\n')
            ans.append('思路：\n')
            for lan in ('C++', 'Java', 'Python'):
                ans.append('<p><strong>{}</strong></p>'.format(lan))
                ans.append('<pre class="lang:{} decode:true ">class Solution(object):</pre>'.format(lan))

        f.writelines('\n'.join(ans))
        f.write('\n\n<br>\n<br>\n本文是leetcode如下的题解<br>\n')
        for t in titles:
            f.write('<li><strong>{}</strong>. {}</li>\n'.format(t[0], t[1]))
        f.write('更多题解可以查看：<a href="https://www.hrwhisper.me/leetcode-algorithm-solution/" target="_blank"> '
                'https://www.hrwhisper.me/leetcode-algorithm-solution/</a>\n<br>\n<br>')


if __name__ == '__main__':
    main(id_list=[796, 797, 798, 799], update_from_leetcode=False)
