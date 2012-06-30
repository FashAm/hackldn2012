from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import User
from app.model.image import PostImage, ImageSize
import base64
import uuid

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

    def check_xsrf_cookie(self): 
        pass

    def on_post(self):        
        path = self.store_images() 
        #Dame to post
        print path
    	self.write('Your photo was successfully fashamified. Very soon other stylish Fashamers will give feedback.')

    def store_images(self):
        '''
        Stores images in the db.
        '''
        try:
            newjpgtxt = self.request.arguments['myImage'][0]
            raw_image = {}
            raw_image['body'] = base64.decodestring(newjpgtxt)
            id = str(uuid.uuid4())
            raw_image['filename'] = "image_"+id+".jpeg"
            image = PostImage()
            size1 = ImageSize()
            size1.size_x = 1200
            size1.size_y = 2048
            size2 = ImageSize()
            size2.size_x = 300
            size2.size_y = 512
            image.sizes = list([size1, size2])
            #image.save()
            return image.store(raw_image, id)
        except Exception, e:
            self.xhr_response = "err,An error occured."
