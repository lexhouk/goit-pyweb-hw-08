from random import randint

from faker import Faker

from connect import init
from services.rabbitmq.models import Contact


def main() -> None:
    if not init() or not (data := init(True)):
        return

    connection, channel, queue_name = data
    fake = Faker()

    for _ in range(randint(10, 20)):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            address=fake.address()
        ).save()

        channel.basic_publish('', queue_name, str(contact.id).encode())

    connection.close()


if __name__ == '__main__':
    main()
