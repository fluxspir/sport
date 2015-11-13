# -*- coding: utf-8 -*-
#

from sportweb import app
from flask import session, render_template, request, redirect, url_for

import sqlalchemy
from wtforms import (Form, BooleanField, TextField, TextAreaField, SelectField,
                    validators)


@app.route('/add_new_place/')
def add_new_place():
    pass

def add_set_to_session():
    return render_template('add_set.html')

@app.route('/swim_session_added/')
def swim_session_add():
    pass
#    form = AddSwimSessionForm(requests.form)

@app.route('/update/')
def update_generic():
    pass

@app.route('/list/')
def list_generic():
    pass
