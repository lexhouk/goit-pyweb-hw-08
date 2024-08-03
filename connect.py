from configparser import ConfigParser, NoOptionError, NoSectionError
from logging import basicConfig, error, INFO
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


def init() -> bool:
    basicConfig(format='%(levelname)s: %(message)s', level=INFO)

    path = Path('credentials.ini')

    try:
        if not path.exists():
            raise Exception(absent('Configuration file', path))

        (config := ConfigParser()).read(path, 'utf-8')

        try:
            credentials = [
                config.get('database', option)
                for option in ('user', 'password', 'host', 'name')
            ]
        except NoSectionError as err:
            raise Exception(absent('Section', err.section))
        except NoOptionError as err:
            raise Exception(absent('Option', err.option))
        else:
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
    except Exception as err:
        error(err)

        return False

    return True
