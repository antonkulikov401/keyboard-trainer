"""This module includes auxiliary functions"""
import functools
from collections.abc import Iterable
from pathlib import Path


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
