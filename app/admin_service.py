from flask import *
from model import *
from pony.orm import *
from Yaml import yml
from Login import md5
from datetime import datetime

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

    article_number = get_number_of_articles()
    try:
        _page_size = min(int(request.args.get("size", 5)), article_number)
        if _page_size <= 0:
            raise ZeroDivisionError
        _cur_page = min(int(request.args.get("page", 1)), article_number // _page_size)
    except ValueError:
        return "page parmas must be int!"
    except ZeroDivisionError:
        return "page size must bigger than zero"

    context = {
        "article_number": article_number,
        "page_size": _page_size,
        "cur_page": _cur_page,
        "text_list": get_page_articles(_cur_page, _page_size),
        "user_list": get_users(),
        "username": username,
        "yml": yml,
    }

    def _update_context():
        article_len = get_number_of_articles()
        context["article_number"] = article_len
        context["text_list"] = get_page_articles(_cur_page, _page_size)

    if request.method == "GET":
        delete_id = int(request.args.get("delete_id", 0))
        if delete_id:  # delete article
            delete_article(delete_id)
            _update_context()
    else:
        data = request.form
        content = data.get("content", "")
        source = data.get("source", "")
        question = data.get("question", "")
        username = data.get("username", "")
        level = data.get("level", "5")
        if content:
            try:    # check level
                if level not in [str(x + 1) for x in range(5)]:
                    raise ValueError
            except ValueError:
                return "level must be between 1 and 5"
            add_article(content, source, level, question)
            _update_context()
        if username:
            update_user_password(username)

    return render_template("admin_index.html", **context)


def add_article(content, source="manual_input", level="5", question="No question"):
    with db_session:
        # add one article to sqlite
        Article(
            text=content,
            source=source,
            date=datetime.now().strftime("%-d %b %Y"),  # format style of `5 Oct 2022`
            level=level,
            question=question,
        )


def delete_article(article_id):
    article_id &= 0xFFFFFFFF  # max 32 bits
    with db_session:
        article = Article.select(article_id=article_id)
        if article:
            article.first().delete()


def get_number_of_articles():
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
        user = User.select(name=username)
        if user and user.first():
            user.first().password = md5(username + password)
