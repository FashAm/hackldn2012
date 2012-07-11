from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import User, UserFriend 
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
        elif self.get_secure_cookie('email'):
            self.redirect('/circles/create')
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
        #self.facebook_request("/me", access_token=user["access_token"], callback=self._save_user_friends)
        uf = UserFriend()
        uf.first_name = "Alexis"
        uf.last_name = "Loizou"
        uf.profile_pic = "http://profile.ak.fbcdn.net/hprofile-ak-snc4/211465_812740366_4006250_n.jpg" 
        uf1 = UserFriend()
        uf1.first_name = "Giorgos"
        uf1.last_name = "Makkoulis"
        uf1.profile_pic = "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/368824_512355977_993007794_n.jpg" 
        friends = [uf, uf1, uf, uf1, uf, uf1, uf, uf1, uf, uf1, uf, uf1, uf, uf1, uf, uf1, uf, uf1, uf, uf1] 
        circles = ["Family", "Friends", "Experts", "Boyfriend", "School"]
        self.base_render("create-circles.html", friends=friends, circles=circles)
        
    def _save_user_friends(self, response):
        '''
        This callback receives "user" which is the response from the API and contains the info for a user's profile.
        '''
        if not user:
            raise tornado.web.HTTPError(500, "Facebook authentication failed.")
        
        
        
class ViewCanvasHandler(base.BaseHandler):
    def on_get(self):
        self.base_render("canvas.html")
    

        