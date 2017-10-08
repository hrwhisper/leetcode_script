# -*- coding: utf-8 -*-
# @Date    : 2017/10/8
# @Author  : hrwhisper
import codecs

from LeetcodeProblemList import LeetcodeProblemList


def main():
    id_list = [691, 693, 694, 695]
    id_list.sort()
    leetcode_list = LeetcodeProblemList().get_list(update_from_leetcode=False)
    with codecs.open('./data/current_solution.html', 'w', 'utf-8') as f:
        titles = [(leetcode_list[_id].number, leetcode_list[_id].title) for _id in id_list]
        f.write('本次题解包括\n')
        for t in titles:
            f.write('<li>{}. {}</li>\n'.format(t[0], t[1]))
        f.write('<!--more-->\n')

        ans = []
        for i, _id in enumerate(id_list):
            cur_problem = leetcode_list[_id]
            print(cur_problem)
            ans.append('<h3>{}. {}</h3>\n\n'.format(int(cur_problem.number), cur_problem.title))
            ans.append('题目地址：<a href="{}" target="_blank" rel="nofollow">leetcode {}</a>' \
                       .format(cur_problem.url, cur_problem.title))
            ans.append('<p>题目大意</p>')
            ans.append('<p>思路</p>')
            ans.append('\n<br>\n<br><hr>\n<br>\n<br>\n')
        f.writelines('\n'.join(ans))
        f.write('本文是leetcode如下的题解<br>\n')
        for t in titles:
            f.write('<li>{}. {}</li>\n'.format(t[0], t[1]))
        f.write('更多题解可以查看：<a href="https://www.hrwhisper.me/leetcode-algorithm-solution/" target="_blank"> '
                'https://www.hrwhisper.me/leetcode-algorithm-solution/</a>\n<br>\n<br>')


if __name__ == '__main__':
    main()
