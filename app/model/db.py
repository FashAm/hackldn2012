from mongoengine import Document, EmailField, StringField, DateTimeField, IntField, EmbeddedDocument, EmbeddedDocumentField

# ============================ User ================================ #
class User(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True)
    email = EmailField(required=True, unique=True)

    def add_user(self, first_name, last_name, username, email):
    	user = User()
    	user.first_name = first_name
    	user.last_name = last_name
    	user.email = email
    	user.username = username

# # ============================ Post ================================ #
# class Post(Document):
#     desc = StringField(required=True, default="")
#     added_on = DateTimeField(required=True, default=datetime.datetime.utcnow)
#     visibility = ListField(StringField(), required=True, default=list)
#     comments = ListField(EmbeddedDocumentField(Comment), default=list)

# class Simple_Post(Post):
# 	url = StringField(required=True, unique=True)


# class Multi_Post(Post):
# 	events = ListField(EmbeddedDocumentField(Images), default=list)

# # ============================ Image ================================ #
# class Images(EmbeddedDocument):
#     url = StringField(required=True, unique=True)
#     votes = IntField(default=0)

# # ============================ Comment ================================ #
# class Comment(EmbeddedDocument):
#     cid = ObjectIdField(required=True)
#     body = StringField(required=True)
#     deleted = BooleanField(default=False)
#     created = DateTimeField(required=True, default=datetime.datetime.utcnow)