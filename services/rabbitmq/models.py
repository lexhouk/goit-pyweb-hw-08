from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, EmailField, \
    EmbeddedDocumentField, StringField


class Email(EmbeddedDocument):
    value = EmailField(required=True)
    delivered = BooleanField(required=True, default=False)


class PhoneNumber(EmbeddedDocument):
    value = StringField(min_length=3, max_length=30, required=True)
    delivered = BooleanField(required=True, default=False)


class Contact(Document):
    fullname = StringField(max_length=50, unique=True, required=True)
    address = StringField(max_length=200)
    email = EmbeddedDocumentField(Email)
    phone_number = EmbeddedDocumentField(PhoneNumber)
    meta = {'collection': 'contacts'}
