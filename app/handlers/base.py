'''
Base handlers.

@author: Alex Michael
'''

import tornado.web, sys, datetime

from mongoengine import ValidationError #@UnresolvedImport
from mongoengine.queryset import OperationError, DoesNotExist #@UnresolvedImport

class BaseHandler(tornado.web.RequestHandler):
    '''
    The base class for all the handlers to inherit. It provides with
    a method of executing the needed operations without needing to deal
    with exception handling.
    
    It also gives the necessary references to the service pool at init time.
    
    An example subclass should look like this:
    
    def ExampleHandler(base.BaseHandler):
    
        def do_get(self):
            ... do code ...
            return param1, param2
            
        def on_success(self, param1, param2):
            self.render("template.html", param1=param1, param2=param2)
    
    The BaseHandler defines defaults for success and error depending on 
    the type of the request:
    (1) If normal request:
        - Success: Do nothing.
        - Error: Raise HTTP 500 error.
    (2) If XHR:
        - Success: Return {"s": true}
        - Error: Return an error response json.
        
    If a handler is used for both normal requests and ajax requests (and hence
    both need to go through on_success), the ajax response can be retrieved 
    from self.xhr_response and updated as necessary. If a need to distinguish
    between the request arises, then self.is_xhr should be of help.
    '''
    def initialize(self):
        '''
        Gives a reference to the current user (if any) to the service pool,
        so that the logged in user is available through self.user to any service.
        
        Also, creates a CachedUser object which stores the three basic properties 
        of the user that are cached throughout the website (id, name, url). If the
        user is not logged in, then None is given to the service pool.
        '''
        #self.services.user = self.current_user
        #self.services.cached_user = self.cached_user
        #self.services.locale = self.locale
        #self.widgets.current_user = self.current_user
        #self.widgets.locale = self.locale
        self.xhr_response = None

    def _(self, text):
        ''' Localisation shortcut '''   
        return self.locale.translate(text).encode("utf-8")

    def get_user_locale(self):
        '''
        Overrides the self.locale.get_user_locale() and gets called automatically.
        Choose the user locale based on the stored attribute.  
        '''
        user_locale = self.current_user and self.current_user.locale or "el_GR"
        return tornado.locale.get(user_locale)

    @property 
    def db(self):
        return self.application.db
    
    #@property
    #def log(self):
    #    return self.application.log
    
    @property
    def deps(self):
        return self.application.deps

    @property
    def env(self):
        return self.application.env
    
    @property
    def widgets(self):
        return self.application.widget_pool
    
    @property
    def services(self):
        return self.application.service_pool
    
    def get(self, *args, **kwargs):
        self._execute_request(self.on_get, *args, **kwargs)
    
    def post(self, *args, **kwargs):
        self._execute_request(self.on_post, *args, **kwargs)
    
    def put(self, *args, **kwargs):
        self._execute_request(self.on_put, *args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self._execute_request(self.on_delete, *args, **kwargs)
    
    def on_get(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)
    
    def on_post(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)
    
    def on_put(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)
    
    def on_delete(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)
    
    def get_current_user(self):
        '''
        Checks if the current user exists and returns it.
        Also set's a reference to a CachedUser object.
        '''
        self.cached_user = None
        cookie = self.get_secure_cookie("email")
        if cookie:
            try: 
                user = User.objects(email=cookie).get()
                cu = CachedUser()
                cu.id = user.id
                cu.name = user.first_name + " " + user.last_name
                cu.url = user.url
                cu.short_desc = user.short_desc
                self.cached_user = cu
                return user
            except DoesNotExist:
                return None
        return None
    
    def write_error(self, status_code, **kwargs):
        '''
        Tornado calls this method when an error occurs. 
        '''
        exc_info = "exc_info" in kwargs["exc_info"] or None
        if status_code == 404:
            self.write("404 error")
        elif status_code == 500:
            if exc_info:
                ex = exc_info[1]
                msg = ex.message.encode("utf-8")
                self.log(msg)
            self.write("500 error")
    
    def base_render(self, template, **kwargs):
        '''
        You should call this method from your handlers to render the template. 
        It takes care of putting the right dependencies in the template. If
        you call Tornado's render() it will crash giving you an error that 
        some variables do not exist.
        '''
        kwargs = kwargs or {}
        kwargs['css_deps'] = self.deps.get("css", self.request.uri)
        kwargs['js_deps']  = self.deps.get("js", self.request.uri)
        kwargs['jqts'] = "{{"
        kwargs['jqte'] = "}}"
        kwargs['env'] = self.env
        kwargs['self'] = self
        
        if self.current_user:
            kwargs['n_count'] = self.services["notification"].get_unread_count(owner=self.current_user.id)
            
        self.render(template, kwargs=kwargs)
    
    def on_success(self, *result):
        raise NotImplementedError()
    
    def on_error(self, ex):
        raise NotImplementedError()
    
    def err_response(self, msg=None):
        '''
        Returns an error-response dictionary, suitable for ajax responses.
        '''
        response = {"s": False}
        if msg:
            response["err"] = msg
        else:
            response["err"] = self._("An error occured. We are working on fixing that now. Please try again.")
        return response
    
    # ======== #
    # PRIVATES #
    # ======== # 
    
    def _execute_request(self, fn, *args, **kwargs):
        try:
            self.is_xhr = self._is_xhr()
            if self.is_xhr:
                self.xhr_response = {"s": True}
            result = fn(*args, **kwargs)
            if result is None:
                result = ()
        except (OperationError, ValidationError), e:
            msg = e.message.encode("utf-8")
            self.log.error(msg)
            self._execute_on_error(e)
        except AjaxMessageException as ame:
            self.log.debug(ame.message)
            self._execute_on_error(ame)
        except tornado.web.HTTPError as httperr:
            self.log.error(str(httperr))
            raise
        except:
            ex = sys.exc_info()[1]
            msg = ex.message.encode("utf-8")
            #self.log.exception(msg)
            self._execute_on_error(ex)
        else:
            self._execute_on_success(*result)
    
    def _execute_on_success(self, *result):
        try:
            if not self._headers_written:
                self.on_success(*result)
        except NotImplementedError:
            if self.is_xhr:
                self._default_xhr_success()
            else:
                self._default_success()
    
    def _execute_on_error(self, ex):
        try:
            if not self._headers_written:
                self.on_error(ex)
        except NotImplementedError:
            if self.is_xhr:
                self._default_xhr_error(ex)
            else:
                self._default_error(ex)
    
    def _default_xhr_success(self):
        '''
        Default behaviour is to write just {"s":true}.
        '''
        self.write(self.xhr_response)
    
    def _default_success(self):
        '''
        No default success behaviour for normal rendering,
        we don't know what to do here.
        '''
        pass
    
    def _default_xhr_error(self, ex):
        '''
        Default behaviour is to write an error response dict. If 
        an AjaxMessageException occured, then the error response
        will contain the exception message as well.
        '''
        if isinstance(ex, AjaxMessageException):
            self.write(self.err_response(msg=str(ex)))
        else:
            self.write(self.err_response())
    
    def _default_error(self, ex):
        '''
        Default behaviour is to throw a 500 error.
        '''
        raise tornado.web.HTTPError(500)
    
    def _is_xhr(self):
        return "X-Requested-With" in self.request.headers \
                and self.request.headers["X-Requested-With"] == "XMLHttpRequest"
    

# ============================ AjaxMessageException ================================ #


class AjaxMessageException(Exception):
    pass


# ============================ WelcomeHandler ================================ #


class WelcomeHandler(BaseHandler):
    '''
    Check user status and either load the home screen or the
    welcome page.
    '''
    def on_get(self):
        #if not self.current_user:
        #    self.base_render("welcome.html")
        #else:
        #    self.redirect("/home")
	self.base_render("welcome.html")


 
# ============================ HomeHandler ================================ #


class HomeHandler(BaseHandler):
    '''
    Load the home screen.
    '''
    def on_get(self):
        #activity = self.services["activity"].get_homepage_items()
        hasParagraph = False
        announcements = []
        # Consider "new" whatever was added within 3 days
        new_fn = lambda p: ((datetime.datetime.utcnow() - p.created).days <= 3) and not p.deleted
        if self.current_user:
            announcements = self.services["announcement"].get_announcements_by_user()
        topics = {}
        for t in Topic.objects.all():
            new = len(self.services['paragraph'].get_new(topic=t.value, new_fn=new_fn))
            topics.setdefault(t.group, []).append((t, new))
        widgets = self.widgets.pick(3, groups=['home'])
        stories = self.services['activity'].get_stories({"published": True}, self.ui["modules"])
	return stories, topics, widgets, announcements, hasParagraph
    
    
    def on_success(self, s, t, w, an, hpa):
        self.base_render("home/home.html", activity_items=s, 
                                           clean=app.tools.sanitize, 
                                           topics = t,
                                           widgets=w,
                                           announcements=an,
                                           hasParagraph = hpa)
