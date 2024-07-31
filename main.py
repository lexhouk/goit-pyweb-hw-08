from configparser import ConfigParser, NoOptionError, NoSectionError
from datetime import datetime
from json import load
from pathlib import Path
from typing import Callable

from mongoengine import connect, Document
from mongoengine.connection import ConnectionFailure
from mongoengine.fields import DateField, ListField, ReferenceField, \
    StringField
from pymongo.errors import ConfigurationError


class Author(Document):
    fullname = StringField(max_length=50, required=True)
    born_date = DateField(required=True)
    born_location = StringField(max_length=100, required=True)
    description = StringField(required=True)
    meta = {'collection': 'authors'}


class Quote(Document):
    tags = ListField(StringField(max_length=30), required=True)
    author = ReferenceField('Author', required=True)
    quote = StringField(required=True)
    meta = {'collection': 'quotes'}


def absent(type: str, name: str) -> None:
    '''Show warning message.

    :param type: Prefix of phrase.
    :param name: Object name which is missed.
    '''
    print(f'{type} {name} not found.')


def collection(
    model: str,
    modify: str,
    modifier: Callable[[str], str],
    key: str = None
) -> dict:
    '''Import documents from file to collection.

    :param model: Class name of collection model.
    :param modify: The dictionary key from the file whose value will be changed
        by the function declared in the next parameter.
    :param modifier: Name of function which will edit file dictionary value
        defined in the previous parameter.
    :param key: (optional) Save created document identifier to function result
        dictionary keyed by value from file dictionary based on a key specified
        in this parameter if last one is defined.

    :return: Document identifiers or empty dictionary.
    '''
    items = {}
    collection = model.lower() + 's'

    try:
        with open(collection + '.json', encoding='utf-8') as file:
            documents = load(file)
    except FileNotFoundError as error:
        absent('Collection file', error.filename)
    else:
        cls = globals()[model]

        for document in documents:
            document[modify] = modifier(document[modify])
            entity = cls(**document).save()

            if key:
                items[document[key]] = entity

        print(f'{len(documents)} documents of {collection} have been '
              'successfully created.')
    finally:
        return items


def main() -> None:
    path = Path('credentials.ini')

    if not path.exists():
        absent('Configuration file', path)
        return

    config = ConfigParser()
    config.read(path, 'utf-8')

    try:
        credentials = [config.get('database', option)
                       for option in ('user', 'password', 'host', 'name')]
    except (NoSectionError, NoOptionError) as error:
        absent(error.__class__.__name__[2:-5], error.section)
    else:
        URI = 'mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority'

        try:
            connect(db=credentials.pop(),
                    host=URI.format(*credentials),
                    tls=True,
                    tlsAllowInvalidCertificates=True)
        except (ConfigurationError, ConnectionFailure):
            print('Invalid credentials.')
        else:
            authors = collection(
                'Author',
                'born_date',
                lambda date: datetime.strptime(date, '%B %d, %Y').date(),
                'fullname'
            )

            collection('Quote', 'author', lambda name: authors[name])


if __name__ == '__main__':
    main()
