#!/usr/bin/env python

from flask import Flask
from flask import Blueprint, g
import models

from gettext import gettext as _
import sys

try:
    from secret import SECRET_KEY, USERNAME, PASSWORD
except:
    print(_("""Please create sport/sport/secret.py with inside :
SECRET_KEY = "somethinghard2find93*9{];;;;eiir!!?|"
USERNAME = "username"
PASSWORD = "password"
"""))
    sys.exit(1)

DEBUG = False

app = Flask(__name__)
app.config.from_object(__name__)

bp = Blueprint('frontend', __name__, url_prefix='/<lang_code>')

models.init()

import sport.views
