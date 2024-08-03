from configparser import ConfigParser, NoOptionError, NoSectionError
from logging import basicConfig, error, INFO
from pathlib import Path


def absent(type: str, name: str = None) -> str:
    '''Show warning message.

    :param type: Prefix of phrase.
    :param name: (optional) Object name which is missed.
    '''

    name = ' ' + name if name else ''

    return f'{type}{name} not found.'


def init(is_rabbitmq: bool = False) -> bool:
    basicConfig(format='%(levelname)s: %(message)s', level=INFO)

    path = Path('credentials.ini')
    section = 'rabbitmq' if is_rabbitmq else 'mongodb'

    try:
        if not path.exists():
            raise Exception(absent('Configuration file', path))

        (config := ConfigParser()).read(path, 'utf-8')

        options = ['user', 'password', 'host']

        if is_rabbitmq:
            options.append('port')

        options.append('name')

        try:
            credentials = [config.get(section, option) for option in options]
        except NoSectionError as err:
            raise Exception(absent('Section', err.section))
        except NoOptionError as err:
            raise Exception(absent('Option', err.option))
        else:
            if is_rabbitmq:
                from services.rabbitmq.connect import handler
            else:
                from services.mongodb.connect import handler

            return handler(credentials)
    except Exception as err:
        error(err)

        return False
