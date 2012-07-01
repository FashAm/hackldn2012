from app.handlers import base
from mongoengine.queryset import DoesNotExist


class ViewTrendsHandler(base.BaseHandler):
    '''

    '''
    def on_get(self):
        self.base_render("view-trends.html")

