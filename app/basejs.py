from jinja2 import Markup

class basejs(object):
    def __init__(self):
        pass

    def render(self, cont):
        return Markup("<script>\ndocument.write(%s);\n</script>"%cont)

    def round(self, num):
        return self.render("round(%s, 1)"%num)

    def fromNow(self):
        return self.render("fromNow()")
