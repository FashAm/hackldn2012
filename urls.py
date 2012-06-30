#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base,home,hello, user, posts, mobile

url_patterns = [
    ("/", home.HomePageHandler),
    ("/hello", hello.HelloHandler),
    ("/login/submit", user.UserLoginHandler),
    ("/login", user.UserLoginOptionsHandler),
    ("/mobile", mobile.OutputPostRequestHandler),
]
