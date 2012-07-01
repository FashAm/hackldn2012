#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base,home,hello, user, post, mobile, trends
import tornado.web
import os

url_patterns = [
    ("/", home.HomePageHandler),
    ("/trending", trends.ViewTrendsHandler),
    ("/login/submit", user.UserLoginHandler),
    ("/mobile", post.PostRequestHandler),
    ("/mobile/feed", mobile.MobileFeedHandler),
    ("/obj/img/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("fashamdata", "img"))}),
]
