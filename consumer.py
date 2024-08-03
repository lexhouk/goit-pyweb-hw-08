from logging import info
from sys import exit

from pika.adapters.blocking_connection import BlockingChannel

from connect import init
from services.rabbitmq.models import Contact


def send(email: str) -> bool:
    '''Stub function.

    :param email: An E-mail address.

    :return: True if a letter has been sent successfully.
    '''
    ...


def callback(channel: BlockingChannel, method, properties, body) -> None:
    if (contact := Contact.objects(id=body.decode(), delivered=False).first()):
        info(f'Sending letter to {contact.email}...')

        send(contact.email)

        contact.update(set__delivered=True)


def main() -> None:
    if not init() or not (data := init(True)):
        return

    _, channel, queue_name = data

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue_name, callback, True)

    info('Waiting for messages. Press CTRL+C to exit.')

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
