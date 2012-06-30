from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import User

class HelloHandler(base.BaseHandler):
    '''
    /hello handler	
    '''
    def on_get(self):
    	#u = User()
    	#u.add_user("Soulis", "Kasapis", "Kreas", "tsoures@egies.mpe")
    	u = User.objects
        self.base_render("hello.html", user = u[0])

