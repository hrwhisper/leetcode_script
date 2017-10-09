# -*- coding: utf-8 -*-
# @Date    : 2017/10/8
# @Author  : hrwhisper

import shutil

from BlogSolutionList import BlogSolutionListUpdate


def add_new_solution(id_dict: dict, update_local=True):
    updater = BlogSolutionListUpdate(update_leetcode=False, update_blog=False, should_statics=True)
    res = updater.create_blog_solution_table_html_code()
    # id_list = [691, 693, 694, 695]
    # solution_url = 'https://www.hrwhisper.me/leetcode-contest-53-solution/'
    for _id, solution_url in id_dict.items():
        res[_id].solution_url = solution_url
        print(res[_id])

    updater.save_in_table(res)
    updater.after_update = res
    updater.statics()
    if update_local:
        shutil.copy('./data/new_blog_solution_table.html', './data/blog_solution_table.html')


def just_add_new_language(id_dict: dict, update_local=True):
    updater = BlogSolutionListUpdate(update_leetcode=False, update_blog=False, should_statics=True)
    res = updater.create_blog_solution_table_html_code()

    for _id, language in id_dict.items():
        res[_id].language = res[_id].language_format(res[_id].language + '/' + language)
        print(res[_id])

    updater.save_in_table(res)
    updater.after_update = res
    updater.statics()

    if update_local:
        shutil.copy('./data/new_blog_solution_table.html', './data/blog_solution_table.html')


if __name__ == '__main__':
    # add_new_solution()
    just_add_new_language({
        326: 'java'
    })
