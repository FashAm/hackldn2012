#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base,home,hello, user

url_patterns = [
    ("/", home.HomePageHandler),
    ("/hello", hello.HelloHandler),
    ("/login/submit", user.UserLoginHandler),
    ("/login", user.UserLoginOptionsHandler),
]
