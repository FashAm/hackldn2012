#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base,home,hello, user, post, mobile, trends
import tornado.web
import os

url_patterns = [
    ("/", home.HomePageHandler),
    #Trending styles handlers
    ("/trending", trends.ViewTrendsHandler),
    #User handlers
    ("/login/submit", user.UserLoginHandler),
    ("/canvas/", user.ViewCanvasHandler),
    #Circles handlers
    ("/circles/create", user.CreateCirclesHandler),
    #Mobile handlers
    ("/mobile", post.PostRequestHandler),
    ("/mobile/feed", mobile.MobileFeedHandler),
    ("/obj/img/(.*)", tornado.web.StaticFileHandler, {"path": os.path.expanduser("~/" + os.path.join("fashamdata", "img"))}),
]
