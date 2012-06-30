#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base,home,hello, user, mobile

url_patterns = [
    ("/", home.HomePageHandler),
    ("/hello", hello.HelloHandler),
    ("/login/user", user.UserLoginHandler),
    ("/logout", user.UserLogoutHandler),
    ("/login", user.UserLogoutHandler),
    ("/mobile", mobile.OutputPostRequestHandler),
]
