from logging import info
from sys import exit
from typing import Callable

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from connect import init
from services.rabbitmq.models import Contact

Handler = Callable[[str], bool]

field: str
type: str
handler: Handler


def callback(
    channel: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes
) -> None:
    '''Messages dispatcher.'''

    sub_field = f'{field}__delivered'
    filters = {'id': body.decode(), sub_field: False}
    contact = Contact.objects(**filters).first()

    if contact:
        recipient = getattr(contact, field).value

        info(f'Sending {type} to {recipient}...')

        if handler(recipient):
            contact.update(**{f'set__{sub_field}': True})


def main() -> None:
    if not init() or not (data := init(True)):
        return

    channel: BlockingChannel = data[1]
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(f'{field}_queue', callback, True)

    [info(msg) for msg in ('Waiting for messages...', 'Press CTRL+C to exit.')]

    channel.start_consuming()


def start(field_name: str, type_name: str, handler_callback: Handler) -> None:
    '''Start listening to some queue.

    :param field_name: The field name.
    :param type_name: The recipient type.
    :param handler_callback: Pointer to function which will process data.
    '''

    global field, type, handler

    field, type, handler = field_name, type_name, handler_callback

    try:
        main()
    except KeyboardInterrupt:
        exit(0)
