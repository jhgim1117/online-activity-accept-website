from flask import render_template, request, redirect
from lib.db import token_insert
import random



def token_post():
    generation, num = request.form["generation"], request.form["num"]
    token_insert(generation, num, random.randint(100000, 999999))
    return render_template('/admin/token.html')
    
def token_get():
    return render_template('/admin/token.html')