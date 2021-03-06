from mongoengine import Document, ObjectIdField, EmbeddedDocument, EmailField, StringField, DateTimeField, IntField, EmbeddedDocument, EmbeddedDocumentField, ListField
import datetime, re
import datetime, os
from PIL import Image
from mongoengine import StringField, EmbeddedDocumentField #@UnresolvedImports 
from mongoengine import ListField, IntField #@UnresolvedImports 
from mongoengine import DateTimeField, ObjectIdField #@UnresolvedImports 
from app.tools import square_image
from app.tools import invalidate_static_url_cache


# ============================ BaseImage ================================ #
class ImageSize(EmbeddedDocument):
    size_x = IntField(required=True, default=600)
    size_y = IntField(required=True, default=1024)

class BaseImage(EmbeddedDocument):
    meta = {"collection": "Images"}
    base_path = StringField(required=True, default=lambda: os.path.expanduser(os.path.join("~/", "fashamdata", "img")))
    created = DateTimeField(required=True, default=datetime.datetime.utcnow)
    type = StringField(required=True, default="image/jpeg")
    sizes = ListField(EmbeddedDocumentField(ImageSize))
    ext = StringField(required=True, default="jpeg")
    rel_path = StringField(required=True)
    url = StringField(required=True, unique=True)
    
    def store(self, data, id):
        filename = data['filename']
        name, ext = os.path.splitext(filename)
        path = self.rel_path+'/'+str(id)+ext  #ORIGINAL IMAGE
        if not os.path.exists(self.rel_path):
            os.makedirs(self.rel_path)
        f = open(path,'w')
        f.write(data['body'])
        f.close()
        
        for size in self.sizes:
            dir = self.rel_path+'/'+str(size.size_x)+'/'+id[-1]+'/'+id[-2]
            if not os.path.exists(dir):
                os.makedirs(dir)
            im = Image.open(path)
            
            # Force RGB.
            if im.mode != 'RGB':
                im = im.convert('RGB')
            tmp_size = size.size_x, size.size_y
            #im = square_image(im)
            #im = im.resize(tmp_size, Image.ANTIALIAS)
            full_path = dir+'/'+id + ".jpg"
            im.save(full_path, "JPEG")

        os.remove(path)
        
        real_path = os.path.expanduser(os.path.join("~/","fashamdata"))
        reg = re.compile(real_path)
        
        return reg.sub("/obj",full_path)
            
# ============================ PostImage ================================ #


class PostImage(BaseImage):
    rel_path = StringField(required=True, default=lambda: os.path.expanduser(os.path.join("~/","fashamdata", "img", "post")))
    sizes = ListField(EmbeddedDocumentField(ImageSize))
    url = StringField(required=True, unique=True)

        
