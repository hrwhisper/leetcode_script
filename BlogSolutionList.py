# -*- coding: utf-8 -*-
# @Date    : 2017/10/8
# @Author  : hrwhisper
import codecs
import requests
from bs4 import BeautifulSoup

from LeetcodeProblemList import LeetcodeProblemInfo, LeetcodeProblemList


class BlogProblemInfo(LeetcodeProblemInfo):
    _order = {
        'C': 0,
        'C++': 1,
        'Java': 2,
        'Python': 3,
        '': 4
    }

    def __init__(self, number, is_ac, title, acceptance, difficulty, solution_url='', language='', is_lock=False):
        super().__init__(number, is_ac, title, acceptance, difficulty, is_lock=is_lock)
        self.solution_url = solution_url
        self.language = self.language_format(language)

    @classmethod
    def language_format(cls, language):  # 让language显示更好看
        return ' / '.join(sorted(filter(lambda x: x, set(map(lambda x: x.strip().title(), language.split('/')))),
                                 key=lambda d: cls._order[d.strip()]))

    def __str__(self):
        return '\t'.join([super().__str__(), self.solution_url, self.language])

    @staticmethod
    def create_from_leetcode_problem_info(info):
        return BlogProblemInfo(info.number, info.is_ac, info.title, info.acceptance, info.difficulty,
                               is_lock=info.is_lock)

    def update(self, info, print_diff_change=False, print_lock_change=False):
        if print_lock_change and info.is_ac and info.is_lock:
            print('{}\t{}'.format(self.number, self.title))

        self.is_ac = info.is_ac
        self.title = info.title
        self.acceptance = info.acceptance
        if print_diff_change and self.difficulty.strip() != info.difficulty.strip():
            print('{}\t{}\t | \t{} -> {}'.format(self.number, self.title, self.difficulty, info.difficulty))
        self.difficulty = info.difficulty
        self.is_lock = info.is_lock
        return self


class BlogSolutionList(object):
    def __init__(self):
        self._blog_solution_html_save_path = './data/blog_solution_table.html'
        self._blog_url = 'https://www.hrwhisper.me/leetcode-algorithm-solution/'

    def _get_html_from_local(self):
        with codecs.open(self._blog_solution_html_save_path, 'r', 'utf-8') as f:
            return f.read()

    def _save_html(self, content):
        with codecs.open(self._blog_solution_html_save_path, 'w', 'utf-8') as f:
            f.write(content)

    def get_list(self, update_from_blog=True):
        problem_list = {}
        if update_from_blog:
            soup = BeautifulSoup(requests.get(self._blog_url).text, "lxml")
            self._save_html(str(soup.find('table')))
        else:
            soup = BeautifulSoup(self._get_html_from_local(), "lxml")
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


class BlogSolutionListUpdate(object):
    def __init__(self, update_leetcode=True, update_blog=True, should_statics=True):
        self.res_save_path = './data/new_blog_solution_table.html'
        self.leetcode_list = self.blog_list = self.after_update = None
        self._update_leetcode = update_leetcode
        self._update_blog = update_blog
        self._should_statics = should_statics

    @staticmethod
    def update_blog_list_from_leetcode_list(leetcode_list: dict, blog_list: dict):
        res = {}
        for _id, info in leetcode_list.items():
            if not info.is_lock:
                if _id not in blog_list:
                    res[_id] = BlogProblemInfo.create_from_leetcode_problem_info(info)
                else:
                    res[_id] = blog_list[_id].update(info)
            else:
                if info.is_ac:  # 以前没加锁的后来加锁的。
                    if _id in blog_list:  # 写过题解
                        res[_id] = blog_list[_id].update(info)
                    else:  # 这个也是以前没加锁的后来加锁的。
                        # print('{}\t{}\t'.format(info.number, info.title))
                        res[_id] = BlogProblemInfo.create_from_leetcode_problem_info(info)
                        # print(_id)
                        # print(set(blog_list.keys()) - set(leetcode_list.keys()))
                        #  {544, 418, 471, 484, 422, 487, 425, 490, 536, 527, 465, 499, 531, 469, 533, 439, 408, 505, 411, 444}
        return res

    def save_in_table(self, res: dict, save_path: str = None):
        if not save_path:
            save_path = self.res_save_path
        with codecs.open(save_path, 'w', 'utf-8') as f:
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
                    if info.is_lock:
                        line.append(
                            '<td><a href="{}" target="_blank">{}</a> <sup><span class="glyphicon glyphicon-lock"></span></sup></td>'
                                .format(info.solution_url, info.title))
                    else:
                        line.append('<td><a href="{}" target="_blank">{}</a></td>'
                                    .format(info.solution_url, info.title))
                else:
                    line.append(('<td>{}</td>'.format(info.title)) if not info.is_lock else
                                '<td>{} <sup><span class="glyphicon glyphicon-lock"></span></sup></td>'.format(
                                    info.title))
                line.append('<td>{}</td>'.format(info.acceptance))
                line.append(('<td>{}</td>'.format(info.difficulty)))
                line.append('<td>{}</td>'.format(info.language))
                line.append('</tr>\n')
                f.writelines(''.join(line))

            f.write('''</tbody>
</table>
</div>''')

    def statics(self):
        total = len(self.leetcode_list)
        lock_number = len(list(filter(lambda x: x.is_lock, self.leetcode_list.values())))
        print('可做总数: {} (题目总数: {} 有锁题数: {})'.format(total - lock_number, total, lock_number))
        ac_number = len(list(filter(lambda x: x.is_ac, self.leetcode_list.values())))
        ac_and_lock_number = len(list(filter(lambda x: x.is_ac and x.is_lock, self.leetcode_list.values())))
        print('AC数目: {}(其中，有锁题目: {})'.format(ac_number, ac_and_lock_number))
        solution_number = len(list(filter(lambda x: x.solution_url, self.after_update.values())))
        print('已发的题解数: {}'.format(solution_number))

    def create_blog_solution_table_html_code(self):
        self.leetcode_list = LeetcodeProblemList().get_list(self._update_leetcode)
        self.blog_list = BlogSolutionList().get_list(self._update_blog)

        self.after_update = self.update_blog_list_from_leetcode_list(self.leetcode_list, self.blog_list)
        # test(res, blog_list)
        self.save_in_table(self.after_update, self.res_save_path)
        if self._should_statics:
            self.statics()
        return self.after_update


if __name__ == '__main__':
    # s = BlogSolutionList()
    # print (s.get_list())
    BlogSolutionListUpdate(update_leetcode=False, update_blog=True).create_blog_solution_table_html_code()
