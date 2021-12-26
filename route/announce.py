from flask import render_template
import datetime
from lib import db

now = datetime.datetime.today()
today = str(now.year)+'-'+str(now.month)+'-'+str(now.day)

def announce_board():
    global today
    allowed_apply_ids = [list(i.values())[0] for i in db.db_execute("SELECT req_id FROM confirmed_apply WHERE allowed=1")]
    allowed_apply_list = list()
    for allowed_apply_id in allowed_apply_ids:
        allowed_apply = db.db_execute("SELECT * FROM apply WHERE req_id=? AND req_date>=?", (allowed_apply_id, today, ))
        if len(allowed_apply):
            allowed_apply_list.append(allowed_apply[0])
    rejected_apply_ids = [list(i.values())[0] for i in db.db_execute("SELECT req_id FROM confirmed_apply WHERE allowed=0")]
    rejected_apply_list = list()
    for rejected_apply_id in rejected_apply_ids:
        rejected_apply = db.db_execute("SELECT * FROM apply WHERE req_id=? AND req_date>=?", (rejected_apply_id, today, ))
        if len(rejected_apply):
            rejected_apply_list.append(rejected_apply[0])
    not_confirmed_apply_ids = [list(i.values())[0] for i in db.db_execute("SELECT req_id FROM apply EXCEPT SELECT req_id FROM confirmed_apply")]
    not_confirmed_apply_list = list()
    for not_confirmed_apply_id in not_confirmed_apply_ids:
        not_confirmed_apply = db.db_execute("SELECT * FROM apply WHERE req_id=? AND req_date>=?", (not_confirmed_apply_id, today, ))
        if len(not_confirmed_apply):
            not_confirmed_apply_list.append(not_confirmed_apply[0])
    return render_template(
        '/announce/announce.html',
        allowed_apply_list = allowed_apply_list,
        rejected_apply_list = rejected_apply_list,
        not_confirmed_apply_list = not_confirmed_apply_list,
        l = max([len(allowed_apply_list), len(rejected_apply_list), len(not_confirmed_apply_list)])
    )
