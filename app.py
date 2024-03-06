#!/usr/bin/python
# -*- coding:utf-8 -*-

#how to run:
#export flask_app=app    <-name of the py file
#export FLASK_ENV=development
#flask run

import flask
import json




app=flask.Flask(__name__)

@app.route("/")
def index():
	return flask.render_template("index.html")

