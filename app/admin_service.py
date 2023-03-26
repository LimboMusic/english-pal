# System Library
from flask import *

# Personal library
from Yaml import yml
from model.user import *
from model.article import *

ADMIN_NAME = "lanhui"  # unique admin name
_cur_page = 1  # current article page
_page_size = 5  # article sizes per page
adminService = Blueprint("admin_service", __name__)


def check_is_admin():
    # 未登录，跳转到未登录界面
    if not session.get("logged_in"):
        return render_template("not_login.html")

    # 用户名不是admin_name
    if session.get("username") != ADMIN_NAME:
        return "You are not admin!"

    return "pass"


@adminService.route("/admin", methods=["GET"])
def admin():
    is_admin = check_is_admin()
    if is_admin != "pass":
        return is_admin

    return render_template(
        "admin_index.html", yml=yml, username=session.get("username")
    )


@adminService.route("/admin/article", methods=["GET", "POST"])
def article():
    global _cur_page, _page_size

    is_admin = check_is_admin()
    if is_admin != "pass":
        return is_admin

    _article_number = get_number_of_articles()
    try:
        _page_size = min(
            max(1, int(request.args.get("size", 5))), _article_number
        )  # 最小的size是1
        _cur_page = min(
            max(1, int(request.args.get("page", 1))), _article_number // _page_size + (_article_number % _page_size > 0)
        )  # 最小的page是1
    except ValueError:
        return "page parmas must be int!"
    
    _articles = get_page_articles(_cur_page, _page_size)
    for article in _articles:   # 获取每篇文章的title
        article.title = article.text.split("\n")[0]
    
    context = {
        "article_number": _article_number,
        "text_list": _articles,
        "page_size": _page_size,
        "cur_page": _cur_page,
        "username": session.get("username"),
    }

    def _update_context():
        article_len = get_number_of_articles()
        context["article_number"] = article_len
        context["text_list"] = get_page_articles(_cur_page, _page_size)
        _articles = get_page_articles(_cur_page, _page_size)
        for article in _articles:   # 获取每篇文章的title
            article.title = article.text.split("\n")[0]
        context["text_list"] = _articles

    if request.method == "GET":
        try:
            delete_id = int(request.args.get("delete_id", 0))
        except:
            return "Delete article ID must be int!"
        if delete_id:  # delete article
            delete_article_by_id(delete_id)
            _update_context()
    elif request.method == "POST":
        data = request.form
        content = data.get("content", "")
        source = data.get("source", "")
        question = data.get("question", "")
        level = data.get("level", "5")
        if content:
            try:  # check level
                if level not in [str(x + 1) for x in range(5)]:
                    raise ValueError
            except ValueError:
                return "Level must be between 1 and 5"
            add_article(content, source, level, question)
            _update_context()
            title = content.split('\n')[0]
            flash(f'Article added. Title: {title}')
    return render_template("admin_manage_article.html", **context)


@adminService.route("/admin/user", methods=["GET", "POST"])
def user():
    is_admin = check_is_admin()
    if is_admin != "pass":
        return is_admin
    
    context = {
        "user_list": get_users(),
        "username": session.get("username"),
    }
    if request.method == "POST":
        data = request.form
        username = data.get("username","")
        new_password = data.get("new_password", "")
        expiry_time = data.get("expiry_time", "")
        if username:
            if new_password:
                update_password_by_username(username, new_password)
                flash(f'Password updated to {new_password}')
            if expiry_time:
                update_expiry_time_by_username(username, "".join(expiry_time.split("-")))
                flash(f'Expiry date updated to {expiry_time}.')
    return render_template("admin_manage_user.html", **context)
