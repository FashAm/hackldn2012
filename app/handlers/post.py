import base64
import uuid
from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import User
from app.model.post import Post
from app.model.image import PostImage, ImageSize
from app.notifier import Twilio

class PostRequestHandler(base.BaseHandler):
    '''
    Render the post request
    '''

    def check_xsrf_cookie(self): 
        pass

    def on_post(self):
        try:
            imgs = []
            for i in range(int(self.request.arguments['numPhotos'][0])):
                img_name = 'myImage' + str(i) 
                imgs.append(self.request.arguments[img_name][0])
            images = self.store_images(imgs) 
            #Create post object
            post = Post()
            post.aid = self.request.arguments['userId'][0]
            
            post.desc = self.request.arguments['description'][0]
            
            for tag in self.request.arguments['tag1'][0].split('\n'):
                post.tags1.append(tag)
            
            for tag in self.request.arguments['tag2'][0].split('\n'):
                post.tags2.append(tag)
                
            phone_no = self.request.arguments['phoneNumber'][0]
            
            for modifier in self.request.arguments['visibility'][0].split(';'):    
                post.visibility.append(modifier)
            
            for image in images:
                post.images.append(image)
            
            post.save()
            self.write('Your photo was successfully fashamified. Very soon other stylish Fashamers will give feedback.')
            
            #Notify the advisors
            #Hacking
            phone_no = phone_no[1:]
            phone_no = "+44" + phone_no
            
            self.notify(customer_name=post.aid, phone_no=phone_no)
        except Exception,e :
            print "Error"+str(e)

    def store_images(self, images):
        '''
        Stores images in the db.
        '''
        try:
            imgs =[]
            for image in images:
                newjpgtxt = image
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
                url = image.store(raw_image, id)
                image.url = url
                imgs.append(image)
            return imgs
        except Exception, e:
            self.xhr_response = "err,An error occured."

    def notify(self, customer_name, phone_no):
        t = Twilio()
        t.send_sms(str(phone_no),'Your friend '+customer_name+" would like your opinion on what to wear. Click here: www.fash.am/help-your-friend .")
