from app.handlers import base
from mongoengine.queryset import DoesNotExist

class HomePageHandler(base.BaseHandler):
    '''
    Renders the home page.	
    '''
    def on_get(self):
        self.base_render("home.html")

