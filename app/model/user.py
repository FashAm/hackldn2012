from mongoengine import Document, ObjectIdField, EmailField, StringField, DateTimeField, IntField, EmbeddedDocument, EmbeddedDocumentField, ListField
import datetime
# ============================ User ================================ #
class User(Document):
    meta = {"collection":"Users"}
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True)
    email = StringField(required=True, unique=True)
    friends = ListField(StringField(), default=list)

    def add_user(self, first_name, last_name, username, email):
    	self.first_name = first_name
    	self.last_name = last_name
    	self.email = email
    	self.username = username
        self.save()
