from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import User 
import tornado.auth, tornado.web

class MobileFeedHandler(base.BaseHandler):
    def on_post(self):
        pass


