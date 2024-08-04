from logging import debug, info, warning
from typing import Any

from redis import StrictRedis
from redis_lru import RedisLRU

from connect import absent, init
from services.mongodb.models import Author, Quote


cache = RedisLRU(StrictRedis('localhost', 6379))


def response(caption: str, names: list, field: list, value: Any) -> str:
    '''Prepare command result.

    :param caption: Prefix of title of quotes list.
    :param names: One or more arguments of the command.
    :param field: Filter condition for selecting specific documents.
    :param value: Field value which is used in a filtering condition.

    :return: Quotes list represented as a single line.
    '''

    debug('Sending query to database...')

    names = ', '.join(names)

    if (quotes := Quote.objects(**{field: value})):
        return '\n'.join([
            f'{caption} {names}:',
            *[f'{key + 1}. {quote.quote}' for key, quote in enumerate(quotes)],
        ])
    else:
        raise Exception(absent(caption, names))


@cache
def name_command(name: str) -> str:
    '''Gets quotes from some authors.

    :param names: Author's full name or some part of it.

    :return: Quotes list represented as a single line.
    '''

    if (authors := Author.objects(fullname__icontains=name)):
        return response(
            'Quotes of author',
            [name],
            'author__in',
            authors
        )
    else:
        raise Exception(absent('Author', name))


@cache
def tag_command(tag: str) -> str:
    '''Gets quotes that have a provided tag.

    :param tag: Tag name or some part of it.

    :return: Quotes list represented as a single line.
    '''

    return response('Quotes with tag', [tag], 'tags__icontains', tag)


def tags_command(tags: str) -> str:
    '''Gets quotes that have provided tags.

    :param tags: Names of tags referenced to quotes that you looking for.

    :return: Quotes list represented as a single line.
    '''

    tags = [formatted for raw in tags.split(',') if (formatted := raw.strip())]

    return response('Quotes with tags', tags, 'tags__in', tags)


def main() -> None:
    '''Infinite loop for reading and processing given commands.'''

    if not init():
        return

    while True:
        command, *arguments = input('Query > ').split(':', 2)

        if (command := command.strip().lower()) == 'exit':
            break
        elif (callback := command + '_command') not in globals().keys():
            warning('Unknown command.')
            continue

        if (arguments := arguments[0].strip() if arguments else None):
            try:
                info(globals()[callback](arguments))
            except Exception as err:
                warning(err)
        else:
            warning(absent(command.title()))


if __name__ == '__main__':
    main()
