from flask import *
from model import *
from pony.orm import *
from Yaml import yml
from Login import md5
from datetime import datetime

# ? from difficulty import text_difficulty_level

ADMIN_NAME = "lanhui"  # unique admin name
_cur_page = 1  # current article page
_page_size = 5  # article sizes per page
adminService = Blueprint("admin_service", __name__)


@adminService.route("/admin", methods=["GET", "POST"])
def admin():
    global _cur_page, _page_size
    # 未登录，跳转到未登录界面
    if not session.get("logged_in"):
        return render_template("not_login.html")

    # 获取session里的用户名
    username = session.get("username")
    if username != ADMIN_NAME:
        return "You are not admin!"

    article_len = get_articles_len()
    try:
        _page_size = min(int(request.args.get("size", 5)), article_len)
        if _page_size <= 0:
            raise ZeroDivisionError
        _cur_page = min(int(request.args.get("page", 1)), article_len // _page_size)
    except ValueError:
        return "page parmas must be int!"
    except ZeroDivisionError:
        return "page size must bigger than zero"

    context = {
        "text_len": article_len,
        "page_size": _page_size,
        "cur_page": _cur_page,
        "text_list": get_page_articles(_cur_page, _page_size),
        "user_list": get_users(),
        "username": username,
        "yml": yml,
    }

    def _update_context():
        article_len = get_articles_len()
        context["text_len"] = article_len
        context["text_list"] = get_page_articles(_cur_page, _page_size)

    if request.method == "GET":
        if delete_id := int(request.args.get("delete_id", 0)):  # delete article
            delete_article(delete_id)
            _update_context()
    else:
        data = request.form
        content = data.get("content", "")
        source = data.get("source", "")
        question = data.get("question", "")
        username = data.get("username", "")
        if content:
            add_article(content, source, question)
            _update_context()
        if username:
            update_user_password(username)

    return render_template("admin_index.html", **context)


def add_article(content, source="manual_input", question="No question"):
    with db_session:
        # add one atricle to sqlite
        Article(
            text=content,
            source=source,
            date=datetime.now().strftime("%-d %b %Y"),  # format style of `5 Oct 2022`
            level="1",
            question=question,
        )
        # ? There is a question that:
        # ? How can i get one article level?
        # ? I try to use the function `text_difficulty_level(content,{"test":1})`
        # ? However, i lose one dict parma from pickle
        # ? So I temporarily fixed the level to 1


def delete_article(article_id):
    article_id &= 0xFFFFFFFF  # max 32 bits
    with db_session:
        if article := Article.select(article_id=article_id):
            article.first().delete()


def get_articles_len():
    with db_session:
        return len(Article.select()[:])


def get_page_articles(num, size):
    with db_session:
        return [
            x
            for x in Article.select().order_by(desc(Article.article_id)).page(num, size)
        ]


def get_users():
    with db_session:
        return User.select()[:]


def update_user_password(username, password="123456"):
    with db_session:
        if if user := User.select(name=username).first():
            user.password = md5(username + password)
