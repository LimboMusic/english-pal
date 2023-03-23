from pony.orm import *

db = Database()
db.bind("sqlite", "../static/wordfreqapp.db", create_db=True)  # bind sqlite file


class User(db.Entity):
    _table_ = "user"  # table name
    name = PrimaryKey(str)
    password = Optional(str)
    start_date = Optional(str)
    expiry_date = Optional(str)


class Article(db.Entity):
    _table_ = "article"  # table name
    article_id = PrimaryKey(int, auto=True)
    text = Optional(str)
    source = Optional(str)
    date = Optional(str)
    level = Optional(str)
    question = Optional(str)


db.generate_mapping(create_tables=True)  # must mapping after class declaration


if __name__ == "__main__":
    with db_session:
        print(Article[2].text)  # test get article which id=2 text content
