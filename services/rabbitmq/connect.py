from pika import BlockingConnection, ConnectionParameters, PlainCredentials


def handler(credentials: list) -> tuple:
    '''Create a connection to the RabbitMQ server.

    :param credentials: Options for connection URI.

    :return: True if it is done without errors.
    '''

    connection = BlockingConnection(
        ConnectionParameters(
            credentials[2],
            credentials[3],
            credentials=PlainCredentials(credentials[0], credentials[1]),
        ),
    )

    channel = connection.channel()

    for name in (names := credentials[4].split(',')):
        name = name.strip().lower()
        channel.exchange_declare(exchange_name := f'{name}_exchange')
        channel.queue_declare(queue_name := f'{name}_queue', durable=True)
        channel.queue_bind(queue_name, exchange_name)

    return connection, channel, names
