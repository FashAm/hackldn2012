from app.handlers import base
from mongoengine.queryset import DoesNotExist

class HelloHandler(base.BaseHandler):
    '''
    /hello handler	
    '''
    def on_get(self):
        self.base_render("hello.html")

