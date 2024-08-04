from random import randint

from faker import Faker

from connect import init

# Embedded documents are called through globals function so they are required.
from services.rabbitmq.models import Contact, Email, PhoneNumber


def main() -> None:
    '''
    Generate a few contacts and put them in different queues depending on the
    type of contact information used.
    '''

    if not init() or not (data := init(True)):
        return

    connection, channel, initial_types = data
    fake = Faker()

    for _ in range(randint(10, 20)):
        fields = {'fullname': fake.name(), 'address': fake.address()}
        types = [*initial_types]

        if (targets := randint(0, 3)):
            for target, field in enumerate(('phone_number', 'email')):
                if targets != target + 1:
                    words = [word.title() for word in field.split('_')]
                    method = getattr(fake, field)
                    fields[field] = globals()[''.join(words)](value=method())
                else:
                    types.remove(field)

        contact = Contact(**fields).save()

        if not targets:
            continue

        message = str(contact.id).encode()

        for type in types:
            channel.basic_publish(f'{type}_exchange', f'{type}_queue', message)

    connection.close()


if __name__ == '__main__':
    main()
