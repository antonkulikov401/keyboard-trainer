"""This module includes auxiliary functions"""
import functools
from collections.abc import Iterable
from pathlib import Path
import os


lang = 'eng'
dicts = {}


def arguments(*args, **kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            return func(*args, **kwargs)
        return wrapper
    return decorator


def all_elements(obj):
    for x in obj:
        if isinstance(x, Iterable) and not isinstance(x, str):
            for y in all_elements(x):
                yield y
        else:
            yield x


def read_stats():
    stats_file = open('stats.log', 'a+')
    stats_file.seek(0)
    stats_raw = stats_file.read().splitlines()
    stats_file.close()
    stats = []
    for stat in stats_raw:
        name, results = stat.split('@')
        v = results.split()
        temp = [(v[i], v[i + 1]) for i in range(0, 10, 2)]
        stats.append((name, temp))
    return stats


def save_lesson(name, text, saved):
    path = Path('./lessons/' + name[0].replace(' ', '_') + '.lesson')
    lesson_file = open(str(path), 'w')
    lesson_file.write(name[0] + '\n')
    lesson_file.write(text[0])
    lesson_file.close()
    saved[0] = True


def load_dicts():
    path = Path('./dicts')
    dict_paths = [str(path / f) for f in os.listdir(str(path)) if
                  f.endswith('.lg')]
    for dict_path in dict_paths:
        dict_file = open(dict_path, 'r')
        dict_content = dict_file.read().splitlines()
        dict_lang = dict_content[0]
        dict_content.pop(0)
        dictionary = {x.split(':')[0]: x.split(':')[1] for x in dict_content}
        dicts[dict_lang] = dictionary
        dict_file.close()


def t(s):
    global lang, dicts
    if lang == 'eng':
        return s
    else:
        return dicts[lang][s]


def set_lang(language, flag=None):
    global lang
    lang = language
    if flag is not None:
        flag[0] = True


def load_heatmap(heat):
    with open('heatmap.log') as file:
        content = file.read().splitlines()
        for line in content:
            symbol, mistakes, total = line.split()
            heat[symbol] = [float(mistakes), float(total)]


def update_heatmap(heat):
    keys = r"""` 1 2 3 4 5 6 7 8 9 0 - = Q W E R T Y U I O P [ ] \ A S D F
    G H J K L ; ' Z X C V B N M , . / @""".split()
    heatmap_file = open('heatmap.log', 'w')
    print(heat)
    for k in keys:
        output = k + ' ' + str(heat[k][0]) + ' ' + str(heat[k][1]) + '\n'
        heatmap_file.write(output)
    heatmap_file.close()
