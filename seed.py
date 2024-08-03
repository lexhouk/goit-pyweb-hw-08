from datetime import datetime
from json import load
from typing import Callable

from connect import absent, init

# Each model should be imported to use them from global definitions.
from services.mongodb.models import Author, Quote


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
        print(absent('Collection file', error.filename))
    else:
        cls = globals()[model]

        for document in documents:
            document[modify] = modifier(document[modify])
            entity = cls(**document).save()

            if key:
                items[document[key]] = entity

        print(
            f'{len(documents)} documents of {collection} have been '
            'successfully created.'
        )
    finally:
        return items


def main() -> None:
    if not init():
        return

    authors = collection(
        'Author',
        'born_date',
        lambda date: datetime.strptime(date, '%B %d, %Y').date(),
        'fullname'
    )

    collection('Quote', 'author', lambda name: authors[name])


if __name__ == '__main__':
    main()
