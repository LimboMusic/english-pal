from model import *
from datetime import datetime

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


def delete_article_by_id(article_id):
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
