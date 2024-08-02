from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path

from mongoengine import connect
from mongoengine.connection import ConnectionFailure
from pymongo.errors import ConfigurationError


def absent(type: str, name: str = None) -> str:
    '''Show warning message.

    :param type: Prefix of phrase.
    :param name: (optional) Object name which is missed.
    '''

    name = ' ' + name if name else ''

    return f'{type}{name} not found.'


def init() -> None:
    path = Path('credentials.ini')

    if not path.exists():
        raise Exception(absent('Configuration file', path))

    config = ConfigParser()
    config.read(path, 'utf-8')

    try:
        credentials = [config.get('database', option)
                       for option in ('user', 'password', 'host', 'name')]
    except (NoSectionError, NoOptionError) as error:
        raise Exception(absent(error.__class__.__name__[2:-5], error.section))
    else:
        URI = 'mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority'

        try:
            connect(db=credentials.pop(),
                    host=URI.format(*credentials),
                    tls=True,
                    tlsAllowInvalidCertificates=True)
        except (ConfigurationError, ConnectionFailure):
            raise Exception('Invalid credentials.')
