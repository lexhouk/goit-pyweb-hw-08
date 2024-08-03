from pickle import dumps
from random import randint

from faker import Faker
from mongoengine import Document
from mongoengine.fields import BooleanField, EmailField, StringField
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from connect import init


class Contact(Document):
    fullname = StringField(max_length=50, required=True)
    email = EmailField(required=True)
    address = StringField(max_length=200)
    delivered = BooleanField(required=True, default=False)
    meta = {'collection': 'contacts'}


def main() -> None:
    if not init():
        return

    connection = BlockingConnection(
        ConnectionParameters(
            'localhost',
            5672,
            credentials=PlainCredentials('guest', 'guest')
        )
    )

    QUEUE = 'subscribers'

    (channel := connection.channel()).queue_declare(QUEUE)

    fake = Faker()

    for _ in range(randint(10, 20)):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            address=fake.address()
        ).save()

        channel.basic_publish('', QUEUE, dumps(contact))

    connection.close()


if __name__ == '__main__':
    main()
