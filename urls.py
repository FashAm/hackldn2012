#############################
# URL patterns.             #
# Author: Giorgos Eracleous #
#############################

from app.handlers import base,home,hello, user, posts

url_patterns = [
    ("/", home.HomePageHandler),
    ("/hello", hello.HelloHandler),
    ("/login/submit", user.UserLoginHandler),
    ("/login", user.UserLoginOptionsHandler),
    ("/mock_image", posts.ViewMockImageHandler),
    ("/mock_image_submit", posts.SubmitMockImageHandler)
]
