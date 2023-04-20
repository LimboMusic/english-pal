from WordFreq import WordFreq
from wordfreqCMD import youdao_link, sort_in_descending_order
from UseSqlite import InsertQuery, RecordQuery
import pickle_idea, pickle_idea2
import os
import random, glob
import hashlib
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for, session, abort, flash, get_flashed_messages
from difficulty import get_difficulty_level, text_difficulty_level, user_difficulty_level


path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment


def total_number_of_essays():
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    rq.instructions("SELECT * FROM article")
    rq.do()
    result = rq.get_results()
    return len(result)


def get_article_title(s):
    return s.split('\n')[0]


def get_article_body(s):
    lst = s.split('\n')
    lst.pop(0)  # remove the first line
    return '\n'.join(lst)


def get_today_article(user_word_list, had_read_articles):
    rq = RecordQuery(path_prefix + 'static/wordfreqapp.db')
    if had_read_articles is None:
        had_read_articles = {
            "index" : 0,  # 为 article_ids 的索引
            "article_ids": []  # 之前显示文章的id列表，越后越新
        }
    if had_read_articles["index"] > len(had_read_articles["article_ids"])-1:
        rq.instructions("SELECT * FROM article")
    else:
        rq.instructions('SELECT * FROM article WHERE article_id=%d' % (had_read_articles["article_ids"][had_read_articles["index"]]))
    rq.do()
    result = rq.get_results()
    random.shuffle(result)

    # Choose article according to reader's level
    d1 = load_freq_history(path_prefix + 'static/frequency/frequency.p')
    d2 = load_freq_history(path_prefix + 'static/words_and_tests.p')
    d3 = get_difficulty_level(d1, d2)

    d = None
    d_user = load_freq_history(user_word_list)
    user_level = user_difficulty_level(d_user, d3)  # more consideration as user's behaviour is dynamic. Time factor should be considered.
    text_level = 0
    if had_read_articles["index"] > len(had_read_articles["article_ids"])-1:  # 下一篇
        flag_get_article = False
        for reading in result:
            text_level = text_difficulty_level(reading['text'], d3)
            factor = random.gauss(0.8,
                                  0.1)  # a number drawn from Gaussian distribution with a mean of 0.8 and a stand deviation of 1
            if reading['article_id'] not in had_read_articles["article_ids"] and within_range(text_level, user_level, (8.0 - user_level) * factor):  # 新的文章之前没有出现过且符合一定范围的水平
                d = reading
                had_read_articles["article_ids"].append(d['article_id'])  # 列表添加新的文章id；下面进行
                flag_get_article = True
                break
        if not flag_get_article:
            had_read_articles["index"] -= 1
    else:  # 上一篇
        d = random.choice(result)
        text_level = text_difficulty_level(d['text'], d3)

    today_article = None
    if d:
        today_article = {
            "user_level": '%4.2f' % user_level,
            "text_level": '%4.2f' % text_level,
            "date": d['date'],
            "article_title": get_article_title(d['text']),
            "article_body": get_article_body(d['text']),
            "source": d["source"],
            "question": get_question_part(d['question']),
            "answer": get_answer_part(d['question'])
        }

    return had_read_articles, today_article


def load_freq_history(path):
    d = {}
    if os.path.exists(path):
        d = pickle_idea.load_record(path)
    return d


def within_range(x, y, r):
    return x > y and abs(x - y) <= r


def get_question_part(s):
    s = s.strip()
    result = []
    flag = 0
    for line in s.split('\n'):
        line = line.strip()
        if line == 'QUESTION':
            result.append(line)
            flag = 1
        elif line == 'ANSWER':
            flag = 0
        elif flag == 1:
            result.append(line)
    return '\n'.join(result)


def get_answer_part(s):
    s = s.strip()
    result = []
    flag = 0
    for line in s.split('\n'):
        line = line.strip()
        if line == 'ANSWER':
            flag = 1
        elif flag == 1:
            result.append(line)
    return '\n'.join(result)
