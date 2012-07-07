from mongoengine import Document, ObjectIdField, EmailField, StringField, DateTimeField, IntField, EmbeddedDocument, EmbeddedDocumentField, ListField
import datetime
# ============================ User ================================ #
class User(Document):
    meta = {"collection":"Users"}
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True)
    email = StringField(required=True, unique=True)
    gender = StringField(required=True)
    locale = StringField(required=True)
    friends = ListField(StringField(), default=list)
    fb_id = StringField(required=True)
    
    def update_token(self, token):
    	self.access_token = token
        self.save()
    
class CachedUser(EmbeddedDocument):
    name = StringField(required=True)
    id = ObjectIdField(required=True)
