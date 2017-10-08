# -*- coding: utf-8 -*-
# @Date    : 2017/10/8
# @Author  : hrwhisper
from BlogSolutionList import BlogSolutionList, BlogSolutionListUpdate


def main():
    updater = BlogSolutionListUpdate(update_leetcode=True, update_blog=True, should_statics=True)
    res = updater.create_blog_solution_table_html_code()
    id_list = [691, 693, 694, 695]
    solution_url = 'https://www.hrwhisper.me/leetcode-contest-53-solution/'
    for _id in id_list:
        res[_id].solution_url = solution_url
        print(res[_id])
    updater.save_in_table(res)
    updater.after_update = res
    updater.statics()


if __name__ == '__main__':
    main()
