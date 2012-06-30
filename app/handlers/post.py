from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.user import User
from app.model.post import Post
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
        for u in users:
            print u
        self.notifier()

    def check_xsrf_cookie(self): 
        pass

    def on_post(self):
        try:
            imgs = []
            for i in range(int(self.request.arguments['numPhotos'][0])):
                img_name = 'myImage' + str(i) 
                imgs.append(self.request.arguments[img_name][0])
            images = self.store_images(imgs) 
            
            post = Post()
            post.aid = self.request.arguments['userId'][0]
            post.desc = self.request.arguments['description'][0]
            post.tags = self.request.arguments['tag']
            post.visibility = self.request.arguments['visibility']
            
            for image in images:
                post.images.append(image)

            post.save()
            self.write('Your photo was successfully fashamified. Very soon other stylish Fashamers will give feedback.')
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
