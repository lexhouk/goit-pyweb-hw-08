from mongoengine import Document
from mongoengine.fields import BooleanField, EmailField, StringField


class Contact(Document):
    fullname = StringField(max_length=50, required=True)
    email = EmailField(required=True)
    address = StringField(max_length=200)
    delivered = BooleanField(required=True, default=False)
    meta = {'collection': 'contacts'}
