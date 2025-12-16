
from mongoengine import Document,StringField,IntField,EmailField


class User(Document):
    name=StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    max_login=IntField(default=0)


class Book(Document):
    title=StringField()
    author=StringField()
    description=StringField()



