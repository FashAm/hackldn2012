from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import User 
import tornado.auth, tornado.web

class UserLoginOptionsHandler(base.BaseHandler):
    def on_get(self):
        self.base_render("login.html")
        
class UserLoginHandler(base.BaseHandler, tornado.auth.FacebookGraphMixin):
    '''
    Handles the login for the Facebook user, returning a user object.
    '''
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
              redirect_uri='http://localhost:8888/login/submit',
              client_id=self.settings["facebook_api_key"],
              client_secret=self.settings["facebook_secret"],
              code=self.get_argument("code"),
              callback=self.async_callback(                                                                                                 
                self._on_login))
            return
        
        self.authorize_redirect(redirect_uri='http://localhost:8888/login/submit',
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "read_stream,offline_access"})
    
    def _on_login(self, user):
        u = User.objects(email=user['link'].encode("utf-8"))
        print user['first_name']
        print user['last_name']
        print user['link']
        if len(u) == 0:
            new_u = User()
            new_u.first_name = user['first_name']
            new_u.last_name = user['last_name']
            new_u.email = user['link'].encode("utf-8")#We couldn't get email so we used user's link 
            new_u.username = new_u.first_name + new_u.last_name
            new_u.save()
            #if not self.get_cookie("email"):
            self.set_secure_cookie("email", new_u.email)

        else:
            u = u.get()            
            #if not self.get_cookie("email"):
            self.set_secure_cookie("email", "change_this_to_the_Real_cookie")
        self.redirect("/")

