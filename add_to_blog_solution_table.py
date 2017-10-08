# -*- coding: utf-8 -*-
# @Date    : 2017/10/8
# @Author  : hrwhisper
from blog_solution_table import create_blog_solution_table_html_code, save_in_table, statics


def main():
    res = create_blog_solution_table_html_code()
    id_list = [691, 693, 694, 695]
    solution_url = 'https://www.hrwhisper.me/leetcode-contest-53-solution/'
    for _id in id_list:
        res[_id].solution_url = solution_url
    save_in_table(res)

if __name__ == '__main__':
    main()
