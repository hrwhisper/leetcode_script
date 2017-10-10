# -*- coding: utf-8 -*-
# @Date    : 2017/10/8
# @Author  : hrwhisper


from BlogSolutionList import BlogSolutionListUpdate


def update_solution(id_dict: dict):
    updater = BlogSolutionListUpdate(update_leetcode=False, update_blog=True, should_statics=True)
    res = updater.create_blog_solution_table_html_code()
    for _id, item in id_dict.items():
        if 'language' in item:
            res[_id].language = res[_id].language_format(res[_id].language + '/' + item['language'])
        if 'solution_url' in item:
            res[_id].solution_url = item['solution_url']
        print(res[_id])

    updater.save_in_table(res)
    updater.after_update = res
    updater.statics()


if __name__ == '__main__':
    # add_new_solution()
    update_solution({
        326: {
            'language': 'java'
        },
        432: {
            'language': 'c++ / java / python',
            'solution_url': 'https://www.hrwhisper.me/leetcode-datastructure/'
        }
    })
