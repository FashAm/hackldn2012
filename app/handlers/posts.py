from app.handlers import base
from mongoengine.queryset import DoesNotExist

class ViewMockImageHandler(base.BaseHandler):
    '''
    Delete this when images are ready.
    '''
    def on_get(self):
        self.base_render("mock_image.html")
        
class SubmitMockImageHandler(base.BaseHandler):
    
    def on_post(self):
        #=======================================================================
        # self.is_xhr = True
        # self.xhr_response = "ok"
        # self.set_header("Content-Type", "text/html")
        #=======================================================================
        approved_file_types = ['.bmp', '.gif', '.jpeg', '.jpg', '.png']
        files = self.request.files
        print files
        if not files:
            self.xhr_response = "err,Please select a file to upload."
        else:
            print 'oulla ok'