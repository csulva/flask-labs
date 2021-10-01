from flask import Flask
from flask.templating import render_template

app = Flask(__name__)


@app.route('/')
def welcome():
    page = "Welcome to Emily's Dog Costumes!"
    return page


@app.route('/services')
def services():
    page = """<p>I offer custom made costumes for your precious canine companion,</p>
        and a free in-home consultation, to get the measurements.</p>"""
    return page


@app.route('/costumes/<costume>')
def costumes(costume):
    page = f"Check out this {costume} costume!"
    return page