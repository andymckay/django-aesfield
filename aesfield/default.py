from django.conf import settings


def lookup(key=None):
    """
    This is the default way to look up the keys for AES. But this is completely
    overridable if you'd like.
    """
    keys = settings.AES_KEYS
    key = 'default' if not key else key
    if key not in keys:
        raise ValueError('Key %s not found.' % key)

    with open(settings.AES_KEYS[key]) as fp:
        return fp.read()
