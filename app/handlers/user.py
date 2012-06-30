from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.db import User 
import tornado.auth, tornado.web

class UserLoginHandler(base.BaseHandler):
    '''
    Handles the login for the Facebook user, returning a user object.
    '''
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
              redirect_uri='http://localhost:8888/register/facebook',
              client_id=self.settings["facebook_api_key"],
              client_secret=self.settings["facebook_secret"],
              code=self.get_argument("code"),
              callback=self.async_callback(
                self._on_login))
            return
        
        self.authorize_redirect(redirect_uri='http://localhost:8888/register/facebook',
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "read_stream,offline_access"})
    
    def _on_login(self, user):
        u = User.objects(email=user['link'])
        if len(u) == 0:
            new_u = User()
            new_u.first_name = user['first_name']
            new_u.last_name = user['last_name']
            new_u.email = user['email'] 
            new_u.username = new_u.first_name + new_u.last_name
            new_u.save()
            self.set_secure_cookie("email", new_u.email)
        else:
            u = u.get()
            self.set_secure_cookie("email", u.email)
        self.redirect("/")
        
class UserLogoutHandler(base.BaseHandler):
    '''
    Logout user.
    '''
    @tornado.web.authenticated
    def on_get(self):
        self.clear_cookie("email")
    
    def on_success(self):
        self.redirect('/')

