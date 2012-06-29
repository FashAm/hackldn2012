#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base,front,hello

url_patterns = [
    ("/", front.FrontPageHandler),
    ("/hello", hello.HelloHandler)
]
