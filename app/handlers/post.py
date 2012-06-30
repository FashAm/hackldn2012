from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.db import User
import base64

class PostRequestHandler(base.BaseHandler):
    '''
    Render the post request
    '''
    def on_get(self):
    	print 'mobile get'
        #Select a hardcoded user for the prototype
        u = self.db.Users.find_one({"username":"GeorgeMakkoulis"})
        #Add some friends
        friends = []
        friends.append({
            "name":"Joanna",
            "phone":"0700000000"
            })
        print friends
        self.db.Users.update({'username':u["username"]},{"$set":{'friends' :friends}});

        print u['username']
        # for u in users:
            # print u
        self.notifier()
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

    def notifier(self):
        #Notify Experts
        #Notify Friends
        print "notifier"
        pass

