from consumer import start


def send(email: str) -> bool:
    '''Stub function.

    :param email: An E-mail address.

    :return: True if a letter has been sent successfully.
    '''

    return True


if __name__ == '__main__':
    start('email', 'letter', send)
