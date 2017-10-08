# -*- coding: utf-8 -*-
# @Date    : 2017/10/3
# @Author  : hrwhisper
import codecs
from pprint import pprint
from bs4 import BeautifulSoup
from hrwhisper_package1.leetcode_spider.LeetcodeProblemList import LeetcodeProblemList, LeetcodeProblemInfo


# class LeetcodeProblemInfoHelper(object):
#     @staticmethod
#     def get_html():
#         # chrome 右键另存为，然后打开Html复制源代码新建一个
#         with open('./data/leetcode.html') as f:
#             return f.read()
#
#     @staticmethod
#     def leetcode_html_parse():
#         problem_list = {}
#
#         soup = BeautifulSoup(LeetcodeProblemInfoHelper.get_html(), "lxml")
#         for tr in soup.find(class_='question-list-table').tbody.find_all('tr'):
#             cur = tr.find_all('td')
#             is_ac = cur[0].has_attr('value')
#             number = cur[1].text
#             title_soup = cur[2]
#             title = title_soup.text.rstrip('New').strip()
#             is_lock = title_soup.find(class_='fa-lock') is not None
#             acceptance = cur[4].text
#             difficulty = cur[5].text
#             # problem_list.append([is_ac, number, title, is_lock, acceptance, difficulty])
#             problem_list[int(number)] = LeetcodeProblemInfo(number, is_ac, title, acceptance, difficulty, is_lock)
#         return problem_list


class BlogProblemInfo(LeetcodeProblemInfo):
    _order = {
        'C': 0,
        'C++': 1,
        'Java': 2,
        'Python': 3,
        '': 4
    }

    def __init__(self, number, is_ac, title, acceptance, difficulty, solution_url='', language=''):
        super().__init__(number, is_ac, title, acceptance, difficulty, is_lock=False)
        self.solution_url = solution_url
        # 让language更好看
        self.language = ' / '.join(sorted(language.strip().title().split('/'), key=lambda d: self._order[d.strip()]))

    def __str__(self):
        return '\t'.join([super().__str__(), self.solution_url, self.language])

    @staticmethod
    def createFromLeetcodeProblemInfo(info):
        return BlogProblemInfo(info.number, info.is_ac, info.title, info.acceptance, info.difficulty)

    def update(self, info, print_diff_change=False, print_lock_change=False):
        if print_lock_change and info.is_ac and info.is_lock:
            print('{}\t{}'.format(self.number, self.title))

        self.is_ac = info.is_ac
        self.title = info.title
        self.acceptance = info.acceptance
        if print_diff_change and self.difficulty.strip() != info.difficulty.strip():
            print('{}\t{}\t | \t{} -> {}'.format(self.number, self.title, self.difficulty, info.difficulty))
        self.difficulty = info.difficulty
        return self


class BlogProblemInfoHelper(object):
    @staticmethod
    def get_html():
        with codecs.open('./data/blog_solution_table.html', 'r', 'utf-8') as f:
            return f.read()

    @staticmethod
    def blog_html_parse():
        problem_list = {}
        soup = BeautifulSoup(BlogProblemInfoHelper.get_html(), "lxml")
        for tr in soup.find('table').tbody.find_all('tr'):
            cur = tr.find_all('td')
            is_ac = cur[0].text.strip() is not ''
            number = cur[1].text
            title_soup = cur[2]
            solution_url = title_soup.a['href'] if title_soup.find('a') else ''
            title = title_soup.text.rstrip('New').strip()
            acceptance = cur[3].text
            difficulty = cur[4].text
            language = cur[5].text
            problem_list[int(number)] = BlogProblemInfo(number, is_ac, title, acceptance, difficulty, solution_url,
                                                        language)
        return problem_list


def merge(leetcode_list: dict, blog_list: dict):
    res = {}
    for _id, info in leetcode_list.items():
        if not info.is_lock:
            if _id not in blog_list:
                res[_id] = BlogProblemInfo.createFromLeetcodeProblemInfo(info)
            else:
                res[_id] = blog_list[_id].update(info)
        else:
            if _id in blog_list:  # 以前没加锁的后来加锁的。
                if blog_list[_id].solution_url:  # 那么需要有题解才保留
                    res[_id] = blog_list[_id].update(info)
            elif info.is_ac and info.is_lock:  # 这个也是以前没加锁的后来加锁的。
                print('{}\t{}\t'.format(info.number, info.title))
                res[_id] = BlogProblemInfo.createFromLeetcodeProblemInfo(info)
                # print(_id)
                # print(set(blog_list.keys()) - set(leetcode_list.keys()))
                #  {544, 418, 471, 484, 422, 487, 425, 490, 536, 527, 465, 499, 531, 469, 533, 439, 408, 505, 411, 444}
    return res


def save_in_table(res):
    with codecs.open('./data/res.html', 'w', 'utf-8') as f:
        f.write('''<div class="table-responsive">
<table class="table table-striped table-centered">
<thead>
<tr><th></th><th>#</th><th>Title</th><th>Acceptance</th><th>Difficulty</th><th>Language</th></tr>
</thead>
<tbody>
''')
        for _, info in sorted(res.items(), reverse=True):
            line = list()
            line.append('<tr><td>{}</td>'.format(' √' if info.is_ac else ''))
            line.append('<td>{}</td>'.format(info.number))
            if info.solution_url:
                line.append('<td><a href="{}" target="_blank">{}</a></td>'.format(info.solution_url, info.title))
            else:
                line.append(('<td>{}</td>'.format(info.title)))
            line.append('<td>{}</td>'.format(info.acceptance))
            line.append(('<td>{}</td>'.format(info.difficulty)))
            line.append('<td>{}</td>'.format(info.language))
            line.append('</tr>\n')
            f.writelines(''.join(line))

        f.write('''</tbody>
</table>
</div>''')


# def test(res, blog_list):  # 看看是否前后的题解相等
#     before_cnt = sum((1 if info.solution_url else 0 for info in blog_list.values()))
#     after_cnt = sum((1 if info.solution_url else 0 for info in res.values()))
#     # print(before_cnt, after_cnt)
#     assert before_cnt == after_cnt

def statics(leetcode_list: dict, blog_list: dict, res: dict):
    total = len(leetcode_list)
    lock_number = len(list(filter(lambda x: x.is_lock, leetcode_list.values())))
    print('可做总数: {} (题目总数: {} 有锁题数: {})'.format(total - lock_number, total, lock_number))
    ac_number = len(list(filter(lambda x: x.is_ac, leetcode_list.values())))
    ac_and_lock_number = len(list(filter(lambda x: x.is_ac and x.is_lock, leetcode_list.values())))
    print('AC数目: {}(其中，有锁题目)'.format(ac_number, ac_and_lock_number))
    solution_number = len(list(filter(lambda x: x.solution_url, res.values())))
    print('已发的题解数: {}'.format(solution_number))


def create_blog_solution_table_html_code(leetcode_list=None, new_list=False):
    if not leetcode_list:
        leetcode_list = LeetcodeProblemList().get_list(new_list)
    # leetcode_list = LeetcodeProblemInfoHelper.leetcode_html_parse()
    blog_list = BlogProblemInfoHelper.blog_html_parse()

    res = merge(leetcode_list, blog_list)
    # test(res, blog_list)
    save_in_table(res)
    statics(leetcode_list, blog_list, res)


if __name__ == '__main__':
    create_blog_solution_table_html_code()
