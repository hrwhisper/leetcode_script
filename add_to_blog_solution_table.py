# -*- coding: utf-8 -*-
# @Date    : 2017/10/8
# @Author  : hrwhisper


from BlogSolutionList import BlogSolutionListUpdate


def _parse(res, _id, item):
    if 'language' in item:
        res[_id].language = res[_id].language_format(res[_id].language + '/' + item['language'])
    if 'solution_url' in item:
        res[_id].solution_url = item['solution_url']
    print(res[_id])


def update_solution(id_dict: dict):
    updater = BlogSolutionListUpdate(update_leetcode=True, update_blog=True, should_statics=True)
    res = updater.create_blog_solution_table_html_code()
    for _ids, item in id_dict.items():
        if isinstance(_ids, tuple):
            for _id in _ids:
                _parse(res, _id, item)
        else:
            _parse(res, _ids, item)

    updater.save_in_table(res)
    updater.after_update = res
    # updater.statics()


if __name__ == '__main__':
    update_solution({
        (1): {
            'language': 'c++ / python / java',
        },
        (712): {
            'solution_url': 'https://www.hrwhisper.me/leetcode-dynamic-programming/',
            'language': 'c++ / python / java',
        }
    })
