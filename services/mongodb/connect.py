from mongoengine import connect
from mongoengine.connection import ConnectionFailure
from pymongo.errors import ConfigurationError


def handler(credentials: list) -> bool:
    '''Create a connection to the MongoDB database.

    :param credentials: Options for connection URI.

    :return: True if it is done without errors.
    '''

    URI = 'mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority'

    try:
        connect(
            db=credentials.pop(),
            host=URI.format(*credentials),
            tls=True,
            tlsAllowInvalidCertificates=True
        )
    except (ConfigurationError, ConnectionFailure):
        raise Exception('Invalid credentials.')

    return True
