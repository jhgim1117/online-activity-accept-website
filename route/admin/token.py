from flask import render_template, request
from lib.db import token_insert
import random

generation, num = request.form["generation"], request.form["num"]

def issue_token(generation, num):
    token_insert(generation, num, token=random.randint(100000, 999999))
    return 
    
def token():
    return render_template('/admin/token.html')