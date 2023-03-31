from model import *
from Login import md5

def get_users():
    with db_session:
        return User.select().order_by(User.name)[:]

def get_user_by_username(username):
    with db_session:
        user = User.select(name=username)
        if user:
            return user.first()

def update_password_by_username(username, password="123456"):
    with db_session:
        user = User.select(name=username)
        if user:
            user.first().password = md5(username + password)

def update_expiry_time_by_username(username, expiry_time="20230323"):
    with db_session:
        user = User.select(name=username)
        if user:
            user.first().expiry_date = expiry_time
