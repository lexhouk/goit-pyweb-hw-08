from configparser import ConfigParser, NoOptionError, NoSectionError
from datetime import datetime
from pathlib import Path

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


def main() -> None:
    path = Path('credentials.ini')

    if not path.exists():
        print(f'Configuration file {path} not found.')
        return

    config = ConfigParser()
    config.read(path, 'utf-8')

    try:
        credentials = [config.get('database', option)
                       for option in ('user', 'password', 'host', 'name')]
    except NoSectionError as error:
        print(f'Section {error.section} not found.')
    except NoOptionError as error:
        print(f'Option {error.option} not found.')
    else:
        QUERY = {
            # 'ssl': 'false',
            'retryWrites': 'true',
            'w': 'majority'
        }

        URI = 'mongodb+srv://{}:{}@{}/?' + \
            '&'.join([f'{key}={value}' for key, value in QUERY.items()])

        try:
            connect(host=URI.format(*credentials),
                    db=credentials.pop(),
                    tls=True,
                    tlsAllowInvalidCertificates=True)
        except (ConfigurationError, ConnectionFailure):
            print('Invalid credentials.')
        else:
            author = Author(fullname='Steve Martin',
                            born_date=datetime(1945, 8, 14),
                            born_location='in Waco, Texas, The United States',
                            description='''Stephen Glenn "Steve" Martin is an
American actor, comedian, writer, playwright, producer, musician, and composer.
He was raised in Southern California in a Baptist family, where his early
influences were working at Disneyland and Knott's Berry Farm and working magic
and comedy acts at these and other smaller venues in the area. His ascent to
fame picked up when he became a writer for the Smothers Brothers Comedy Hour,
and later became a frequent guest on the Tonight Show.In the 1970s, Martin
performed his offbeat, absurdist comedy routines before packed houses on
national tours. In the 1980s, having branched away from stand-up comedy, he
became a successful actor, playwright, and juggler, and eventually earned Emmy,
Grammy, and American Comedy awards.''')

            author.save()

            Quote(tags=('humor', 'obvious', 'simile'),
                  author=author,
                  quote='A day without sunshine is like, you know, night.'
                  ).save()


if __name__ == '__main__':
    main()
