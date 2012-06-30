import datetime
from mongoengine import Document, ObjectIdField, EmailField, StringField, DateTimeField, IntField, EmbeddedDocument, EmbeddedDocumentField, ListField
from app.model.image import PostImage

# ============================ Comment ================================ #
class Comment(EmbeddedDocument):
    meta = {"collection":"Comments"}
    aid = ObjectIdField(required=True)
    body = StringField(required=True)
    created = DateTimeField(required=True, default=datetime.datetime.utcnow)

# ============================ Post ================================ #
class Post(Document):
    meta = {"collection":"Posts"}
    aid = StringField(required=True)
    desc = StringField(required=True, default="")
    added_on = DateTimeField(required=True, default=datetime.datetime.utcnow)
    visibility = ListField(StringField(), required=True, default=list)
    comments = ListField(EmbeddedDocumentField(Comment), default=list)
    decision = StringField(required=True, default="")
    tags = ListField(StringField(), required=True, default=list)
    images = ListField(EmbeddedDocumentField(PostImage), required=True, default=list)



