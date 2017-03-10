from flask import render_template as flask_render_template
from rjscssmin_plugin import html_minify

def render_template(*args, **kwargs):
    res = flask_render_template(*args, **kwargs)
    return html_minify(res)
