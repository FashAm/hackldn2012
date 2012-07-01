from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.post import Post

class HomePageHandler(base.BaseHandler):
    '''
    Renders the home page.	
    '''
    def on_get(self):
        posts = Post.objects.order_by('-added_on')
        self.base_render("home.html", posts=posts)

