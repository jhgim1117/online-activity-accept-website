from flask import render_template
from lib import db

user_list_in_db = db.db_execute("SELECT * FROM user")

def show_user_list():
    return render_template(
        'user/user_list.html',
        user_list = user_list_in_db
    )