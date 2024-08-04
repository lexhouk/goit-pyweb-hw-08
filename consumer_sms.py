from consumer import start


def send(phone_number: str) -> bool:
    '''Stub function.

    :param phone_number: A phone number.

    :return: True if a SMS has been sent successfully.
    '''

    return True


if __name__ == '__main__':
    start('phone_number', 'SMS', send)
