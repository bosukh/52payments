from . import render_template
from flask.views import View

class StaticView(View):
    methods = ['GET']
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)
