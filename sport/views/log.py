# -*- coding: utf-8 -*-
#

from flask import session, render_template, request, redirect, url_for
import sqlalchemy
from models import meta
from secret import SECRET_KEY
from sportweb import app

#from odontux import constants, checks

from gettext import gettext as _

@app.route('/')
def index():
    return render_template('index.html')

app.secret_key = SECRET_KEY
