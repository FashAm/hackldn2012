from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import User, UserCircle 
import tornado.auth, tornado.web
from tornado import httpclient
import functools

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
        try:
            c_user = User.objects(access_token=user['access_token']).get()
        except DoesNotExist, e:   
            c_user = User()
            c_user.access_token = user["access_token"]        
            cb = functools.partial(self._save_user_profile, c_user)
            self.facebook_request("/me", access_token=c_user.access_token, callback=cb)
            
            cb = functools.partial(self._save_user_friends, c_user)
            self.facebook_request("/me/friends", access_token=c_user.access_token, callback=cb, fields='first_name,last_name,id,picture')
            
        self.set_secure_cookie("access_token", c_user.access_token)
        self.redirect("/")   
    
    def _save_user_profile(self, c_user, response):
        '''
        This callback receives "user" which is the response from the API and contains the info for a user's profile.
        '''
        if not response:
            raise tornado.web.HTTPError(500, "Facebook authentication failed.")

        c_user.first_name = response['first_name']
        c_user.last_name = response['last_name']
        c_user.email = response['email'] 
        c_user.username = response['username']
        c_user.gender = response['gender']
        c_user.locale = response['locale']
        c_user.fb_id = response['id']
        c_user.save()    

    def _save_user_friends(self, c_user, response):
        '''
        This callback receives the response from the API that contains user's friends.
        '''
        if not c_user:
            raise tornado.web.HTTPError(500, "Facebook authentication failed.")
        friends = response['data']
        for friend in friends:
            uf = UserFriend()
            uf.first_name = friend['first_name']
            uf.last_name = friend['last_name']
            uf.profile_pic = friend['picture']
            uf.fb_id = friend['id']
            c_user.friends.append(uf)
        c_user.save()
    
class CreateCirclesHandler(base.BaseHandler, tornado.auth.FacebookGraphMixin):
    '''                    
    This handler allows the user to create circles to share their
    photos with.
    '''
    def on_get(self):
        #=======================================================================
        # uc = UserCircle()
        # uc.name = "Family"
        # uc1 = UserCircle()
        # uc1.name = "Friends"
        # uc2 = UserCircle()
        # uc2.name = "Experts"
        # self.current_user.circles.append(uc1)
        # self.current_user.save()
        #=======================================================================
        self.base_render("create-circles.html", friends=self.current_user.friends, circles=self.current_user.circles)
        
        
class ViewCanvasHandler(base.BaseHandler):
    def on_get(self):
        self.base_render("canvas.html")
    

        