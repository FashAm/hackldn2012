#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base,home,hello, user, post, mobile
import tornado.web
import os

url_patterns = [
    ("/", home.HomePageHandler),
    ("/hello", hello.HelloHandler),
    ("/login/submit", user.UserLoginHandler),
    ("/mobile", post.PostRequestHandler),
    ("/mobile/feed", mobile.MobileFeedHandler),
    ("/obj/img/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("fashamdata", "img"))}),
]
