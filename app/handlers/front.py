from app.handlers import base
from mongoengine.queryset import DoesNotExist

class FrontPageHandler(base.BaseHandler):
    '''
    Renders the home page.	
    '''
    def on_get(self):
        self.base_render("intro.html")

