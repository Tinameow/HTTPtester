# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False



from . import projects, testcases, files, tests