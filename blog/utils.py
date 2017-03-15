import random

def generate_filename(prefix=None, length=10):
    '''
    Returns generated filename, if the slugify is empty.
    '''
    characters = (
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        'abcdefghijklmnopqrstuvwxyz'
        '0123456789'
    )

    filename = prefix if not prefix is None else ''

    for _ in range(length):
        filename += random.choice(characters)
    return filename