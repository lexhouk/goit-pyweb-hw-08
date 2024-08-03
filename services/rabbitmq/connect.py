from pika import BlockingConnection, ConnectionParameters, PlainCredentials


def handler(credentials: list) -> tuple:
    connection = BlockingConnection(
        ConnectionParameters(
            credentials[2],
            credentials[3],
            credentials=PlainCredentials(credentials[0], credentials[1]),
        ),
    )

    channel = connection.channel()
    channel.queue_declare(credentials[4], durable=True)

    return connection, channel, credentials[4]
