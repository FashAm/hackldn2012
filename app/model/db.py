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

# ============================ Image ================================ #
class Images(EmbeddedDocument):
    meta = {"collection":"Images"}
    url = StringField(required=True, unique=True)
    votes = IntField(default=0)

# ============================ Comment ================================ #
class Comment(EmbeddedDocument):
    meta = {"collection":"Comments"}
    aid = ObjectIdField(required=True)
    body = StringField(required=True)
    created = DateTimeField(required=True, default=datetime.datetime.utcnow)

# ============================ Post ================================ #
class Post(Document):
    meta = {"collection":"Posts"}
    aid = ObjectIdField(required=True)
    desc = StringField(required=True, default="")
    added_on = DateTimeField(required=True, default=datetime.datetime.utcnow)
    tags = ListField(StringField(), required=True, default=list)
    visibility = ListField(StringField(), required=True, default=list)
    comments = ListField(EmbeddedDocumentField(Comment), default=list)
    decision = StringField(required=True, default="")

class Simple_Post(Post):
	url = StringField(required=True, unique=True)

class Multi_Post(Post):
	events = ListField(EmbeddedDocumentField(Images), default=list)


