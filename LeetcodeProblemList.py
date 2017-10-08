# -*- coding: utf-8 -*-
# @Date    : 2017/10/4
# @Author  : hrwhisper
import codecs
import json

from hrwhisper_package1.leetcode_spider.LoginLeetcode import LoginLeetcode


class LeetcodeProblemInfo(object):
    def __init__(self, number, is_ac, title, acceptance, difficulty, is_lock=False):
        self.number = number
        self.is_ac = is_ac
        self.title = title
        self.acceptance = acceptance
        self.difficulty = difficulty
        self.is_lock = is_lock

    def __str__(self):
        return '\t'.join(map(str,[self.number, self.is_ac, self.title, self.acceptance, self.difficulty]))


class LeetcodeProblemList(LoginLeetcode):
    def __init__(self):
        super().__init__()
        self.problem_list_save_path = './data/leetcode_problem_list.txt'
        self._level2difficult = {1: 'Easy', 2: 'Medium', 3: 'Hard'}

    def _get_problem_list(self, save=True):
        """

        :param save:
        :param page_num:
        :return:
        """
        self.login()
        res = self.session.get('https://leetcode.com/api/problems/algorithms/', headers=self.my_head).text
        if save:
            with codecs.open(self.problem_list_save_path, 'w', 'utf-8') as f:
                f.write(res)
        return res

    def get_list(self, update_from_leetcode=True):
        """
        parse list to dict{number: LeetcodeProblemInfo} from the followings:
        {"status": "ac", "stat": {"total_acs": 2615, "question__title": "Employee Importance", "is_new_question": true, "question__article__slug": null, "total_submitted": 4436, "question__title_slug": "employee-importance", "question__article__live": null, "question__hide": false, "question_id": 690}, "is_favor": false, "paid_only": false, "difficulty": {"level": 1}, "frequency": 0, "progress": 0}
        :param update_from_leetcode: using data which get from leetcode.com or the content save before.
        :return: dict{number: LeetcodeProblemInfo}
        """
        if update_from_leetcode:
            res = self._get_problem_list()
        else:
            with codecs.open(self.problem_list_save_path, 'r', 'utf-8') as f:
                res = f.read()
        d = json.loads(res)['stat_status_pairs']
        res = {}
        for cur in d:
            is_ac = cur['status'] == 'ac'
            number = cur['stat']['question_id']
            title = cur['stat']['question__title']
            acceptance = '{0:.1f}%'.format(cur['stat']['total_acs'] / cur['stat']['total_submitted'] * 100)
            difficulty = self._level2difficult[cur['difficulty']['level']]
            is_lock = cur['paid_only']
            res[int(number)] = LeetcodeProblemInfo(number, is_ac, title, acceptance, difficulty, is_lock)
        return res


if __name__ == '__main__':
    s = LeetcodeProblemList()
    s.parse_list()
