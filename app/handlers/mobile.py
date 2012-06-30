from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.db import User
import base64

class OutputPostRequestHandler(base.BaseHandler):
    '''
    Render the post request
    '''
    def on_get(self):
    	print 'koukou'
        self.base_render("mobile.html", user = 'hii')

    def check_xsrf_cookie(self): 
        pass

    def on_post(self):
        newjpgtxt = self.request.arguments['myImage'][0]
        # print newjpgtxt
    	g = open("out.jpg", "w")
    	g.write(base64.decodestring(newjpgtxt))
    	g.close()
        #Response back text
    	self.write('pampos')

