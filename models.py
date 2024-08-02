from mongoengine import Document
from mongoengine.fields import DateField, ListField, ReferenceField, \
    StringField


class Author(Document):
    fullname = StringField(max_length=50, required=True)
    born_date = DateField(required=True)
    born_location = StringField(max_length=100, required=True)
    description = StringField(required=True)
    meta = {'collection': 'authors'}


class Quote(Document):
    tags = ListField(StringField(max_length=30), required=True)
    author = ReferenceField('Author', required=True)
    quote = StringField(required=True)
    meta = {'collection': 'quotes'}
