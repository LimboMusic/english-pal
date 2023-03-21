from datetime import datetime

from flask import *

# from app import Yaml
# from app.Article import get_today_article, load_freq_history
# from app.WordFreq import WordFreq
# from app.wordfreqCMD import sort_in_descending_order

import Yaml
from Article import get_today_article, load_freq_history
from WordFreq import WordFreq
from wordfreqCMD import sort_in_descending_order

import pickle_idea
import pickle_idea2

# 初始化蓝图
userService = Blueprint("user_bp", __name__)

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment


@userService.route("/<username>/reset", methods=['GET', 'POST'])
def user_reset(username):
    '''
    用户界面
    :param username: 用户名
    :return: 返回页面内容
    '''
    if request.method == 'GET':
        existing_articles = session.get("existing_articles")
        existing_articles[0] += 1
        session["existing_articles"] = existing_articles
        return redirect(url_for('user_bp.userpage', username=username))
    else:
        return 'Under construction'

@userService.route("/<username>/back", methods=['GET'])
def user_back(username):
    '''
    用户界面
    :param username: 用户名
    :return: 返回页面内容
    '''
    if request.method == 'GET':
        existing_articles = session.get("existing_articles")
        existing_articles[0] -= 1
        session["existing_articles"] = existing_articles
        return redirect(url_for('user_bp.userpage', username=username))



@userService.route("/<username>/<word>/unfamiliar", methods=['GET', 'POST'])
def unfamiliar(username, word):
    '''

    :param username:
    :param word:
    :return:
    '''
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.unfamiliar(user_freq_record, word)
    session['thisWord'] = word  # 1. put a word into session
    session['time'] = 1
    return "success"


@userService.route("/<username>/<word>/familiar", methods=['GET', 'POST'])
def familiar(username, word):
    '''

    :param username:
    :param word:
    :return:
    '''
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.familiar(user_freq_record, word)
    session['thisWord'] = word  # 1. put a word into session
    session['time'] = 1
    return "success"


@userService.route("/<username>/<word>/del", methods=['GET', 'POST'])
def deleteword(username, word):
    '''
    删除单词
    :param username: 用户名
    :param word: 单词
    :return: 重定位到用户界面
    '''
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea2.deleteRecord(user_freq_record, word)
    # 模板 userpage_get.html 中已经没有对flash信息的获取了，而且会影响 signup.html的显示，因为其中去获取了flash。在删除单词，退出，注册，页面就会出现提示信息
    # flash(f'<strong>{word}</strong> is no longer in your word list.')
    return "success"


@userService.route("/<username>", methods=['GET', 'POST'])
def userpage(username):
    '''
    用户界面
    :param username: 用户名
    :return: 返回用户界面
    '''
    # 未登录，跳转到未登录界面
    if not session.get('logged_in'):
        return render_template('not_login.html')

    # 用户过期
    user_expiry_date = session.get('expiry_date')
    if datetime.now().strftime('%Y%m%d') > user_expiry_date:
        return render_template('expiry.html', expiry_date=user_expiry_date)

    # 获取session里的用户名
    username = session.get('username')

    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)

    if request.method == 'POST':  # when we submit a form
        content = escape(request.form['content'])
        f = WordFreq(content)
        lst = f.get_freq()
        return render_template('userpage_post.html',username=username,lst = lst, yml=Yaml.yml)

    elif request.method == 'GET':  # when we load a html page
        d = load_freq_history(user_freq_record)
        lst = pickle_idea2.dict2lst(d)
        lst2 = []
        for t in lst:
            lst2.append((t[0], len(t[1])))
        lst3 = sort_in_descending_order(lst2)
        words = ''
        for x in lst3:
            words += x[0] + ' '
        existing_articles, today_article = get_today_article(user_freq_record, session.get('existing_articles'))
        session['existing_articles'] = existing_articles
        # 通过 today_article，加载前端的显示页面
        return render_template('userpage_get.html',
                               username=username,
                               session=session,
                               flashed_messages=get_flashed_messages(),
                               today_article=today_article,
                               d_len=len(d),
                               lst3=lst3,
                               yml=Yaml.yml,
                               words=words)





@userService.route("/<username>/mark", methods=['GET', 'POST'])
def user_mark_word(username):
    '''
    标记单词
    :param username: 用户名
    :return: 重定位到用户界面
    '''
    username = session[username]
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    if request.method == 'POST':
        # 提交标记的单词
        d = load_freq_history(user_freq_record)
        lst_history = pickle_idea2.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, [get_time()]))
        d = pickle_idea2.merge_frequency(lst, lst_history)
        pickle_idea2.save_frequency_to_pickle(d, user_freq_record)
        return redirect(url_for('user_bp.userpage', username=username))
    else:
        return 'Under construction'

def get_time():
    '''
    获取当前时间
    :return: 当前时间
    '''
    return datetime.now().strftime('%Y%m%d%H%M')  # upper to minutes

