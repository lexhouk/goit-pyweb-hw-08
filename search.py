from logging import info, warning
from typing import Any

from connect import absent, init
from services.mongodb.models import Author, Quote


def response(caption: str, names: list, field: list, value: Any) -> str:
    names = ', '.join(names)

    if (quotes := Quote.objects(**{field: value})):
        return f'{caption} {names}:\n' + \
            '\n'.join([
                f'{delta + 1}. {quote.quote}'
                for delta, quote in enumerate(quotes)
            ])
    else:
        raise Exception(absent(caption, names))


def name_command(arguments: list) -> str:
    name, *_ = arguments

    if (authors := Author.objects(fullname=name)):
        return response(
            'Quotes of author',
            [name],
            'author__in',
            authors
        )
    else:
        raise Exception(absent('Author', name))


def tag_command(arguments: list) -> str:
    tag, *_ = arguments

    return response('Quotes with tag', [tag], 'tags', tag)


def tags_command(arguments: list) -> str:
    return response(
        'Quotes with tags',
        arguments,
        'tags__in',
        arguments
    )


def main() -> None:
    if not init():
        return

    while True:
        command, *arguments = input('Query > ').split(':', 2)

        if (command := command.strip().lower()) == 'exit':
            break
        elif (callback := command + '_command') not in globals().keys():
            warning('Unknown command.')
            continue

        if arguments:
            arguments = [
                argument.strip()
                for argument in arguments[0].split(',')
                if argument.strip()
            ]

        if arguments:
            try:
                info(globals()[callback](arguments))
            except Exception as err:
                warning(err)
        else:
            warning(absent(command.title()))


if __name__ == '__main__':
    main()
