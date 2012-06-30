from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.db import User
from app.model.image import ProfileImage, ImageSize
import base64
import uuid

class PostRequestHandler(base.BaseHandler):
    '''
    Render the post request
    '''
    def on_get(self):
        self.base_render("mobile.html", user = 'hii')

    def check_xsrf_cookie(self): 
        pass

    def on_post(self):
        newjpgtxt = self.request.arguments['myImage'][0]
        raw_image = {}
        raw_image['body'] = base64.decodestring(newjpgtxt)
        id = str(uuid.uuid4())
        raw_image['filename'] = "image_"+id+".jpeg"
        self.store_images(raw_image, id) 
    	self.write('Your photo was successfully fashamified. Very soon other stylish Fashamers will give feedback.')

    def store_images(self, raw_image, id):
        '''
        Stores images in the db.
        '''
        try:
            image = ProfileImage()
            size1 = ImageSize()
            size1.size_x = 576
            size1.size_y = 1024
            size2 = ImageSize()
            size2.size_x = 300
            size2.size_y = 512
            image.sizes = list([size1, size2])
            #image.save()
            image.store(raw_image, id)
        except Exception, e:
            self.xhr_response = "err,An error occured."