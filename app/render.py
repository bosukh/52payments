import logging
from flask import render_template as flask_render_template
from flask import render_template_string
from htmlmin import minify
from rcssmin import _make_cssmin
from rjsmin import _make_jsmin
from config import basedir

def render_template(*args, **kargs):
    res = flask_render_template(*args, **kargs)
    #res = render_template_string(res)
    return minify(res)

def minify_css(string_obj):
    cssmin = _make_cssmin(python_only=True)
    return cssmin(string_obj)

def minify_js(string_obj):
    jsmin = _make_jsmin(python_only=True)
    return jsmin(string_obj)

class minified_files:
    def __init__(self):
        self.js, self.css= {}, {}
        from os import listdir
        from codecs import open
        for jsfile in listdir(basedir+'/app/static/js'):
            if len(jsfile.split('.')) == 2 and jsfile[-2:] == 'js':
                temp = open(basedir+'/app/static/js/' + jsfile, encoding="utf-8")
                self.js[jsfile] = temp.read()
        for cssfile in listdir(basedir+'/app/static/css'):
            if len(cssfile.split('.')) == 2 and cssfile[-3:] == 'css':
                temp = open(basedir+'/app/static/css/' + cssfile, encoding="utf-8")
                self.css[cssfile] = temp.read()
    def include_js(self, *args):
        stored = self.js.get(str(args))
        if stored:
            return stored
        js = ""
        for arg in args:
            js += self.js.get(arg, '')
        js = '<script type="text/javascript">%s</script>'%minify_js(js)
        self.js[str(args)] = js
        return js

    def include_css(self, *args):
        stored = self.css.get(str(args))
        if stored:
            return stored
        css = ""
        for arg in args:
            logging.debug(self.css)
            css += self.css.get(arg, '')
        css = '<style media="screen">%s</style>'%minify_css(css)
        self.css[str(args)] = css
        return css
