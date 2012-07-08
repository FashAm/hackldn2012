from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import User 
import tornado.auth, tornado.web
from tornado import httpclient

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
                                extra_params={"scope": "email"})
    
    def _on_login(self, user):
        self.facebook_request("/me", access_token=user["access_token"], callback=self._save_user_profile)
        self.redirect("/")
        
    def _save_user_profile(self, user):
        '''
        This callback receives "user" which is the response from the API and contains the info for a user's profile.
        '''
        if not user:
            raise tornado.web.HTTPError(500, "Facebook authentication failed.")
        try:
            User.objects(email=user['email']).get()
        except DoesNotExist, e:            
            new_u = User()
            new_u.first_name = user['first_name']
            new_u.last_name = user['last_name']
            new_u.email = user['email'] 
            self.set_secure_cookie("email", new_u.email)   
            new_u.username = user['username']
            new_u.gender = user['gender']
            new_u.locale = user['locale']
            new_u.fb_id = user['id']
            new_u.save()    
        else:
            #User exists
            pass
    
class CreateCirclesHandler(base.BaseHandler):
    '''                    
    This handler allows the user to create circles to share their
    photos with.
    '''
    def on_get(self):
        self.base_render("create-circles.html")

        