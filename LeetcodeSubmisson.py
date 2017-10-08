# -*- coding: utf-8 -*-
# @Date    : 2017/10/4
# @Author  : hrwhisper
import codecs
import json

from LoginLeetcode import LoginLeetcode


class LeetcodeSubmisson(LoginLeetcode):
    """
        给定题目的名称，从leetcode的提交记录中查找提交的记录，并打印
    """

    def __init__(self):
        super().__init__()
        self.submission_save_path = './data/submission.txt'

    def get_submisson_res(self, save=True, page_num=1000):
        """

        :param save:
        :param page_num:
        :return: a string. can convert to json
        """
        self.login()
        res = self.session.get('https://leetcode.com/api/submissions/?offset=0&limit={}'.format(page_num)).text
        if save:
            with codecs.open(self.submission_save_path, 'w', 'utf-8') as f:
                f.write(res)
        return res

    def find(self, name: set, get_new=True):
        if get_new:
            res = self.get_submisson_res()
        else:
            with codecs.open(self.submission_save_path, 'r', 'utf-8') as f:
                res = f.read()
        d = json.loads(res)['submissions_dump']
        for cur in d:
            if cur['title'] in name:
                print('{} {} https://leetcode.com{}'.format(cur['title'], cur['status_display'], cur['url']))


if __name__ == '__main__':
    s = LeetcodeSubmisson()
    s.find({'Kill Process', 'Remove 9', 'Equal Tree Partition'}, get_new=False)
