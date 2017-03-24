import os
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


def generate_key(byte_length):
    """
    Return a true random ascii string that is byte_length long.
    The resulting key is suitable for cryptogrpahy.
    """
    if byte_length < 32:
        raise ValueError('um, %s is probably not long enough for cryptography'
                         % byte_length)
    return os.urandom(byte_length).encode('hex')


class Command(BaseCommand):
    help = 'Generate a randomized encryption encryption key'

    def add_arguments(self, parser):
        parser.add_argument(
            '--length', action='store', type=int, dest='length',
            help='Key length in bytes. Default: %(default)',
            default=128)

    def handle(self, *args, **options):
        failures = False
        for dest in settings.AES_KEYS.values():
            if os.path.exists(dest):
                failures = True

                self.stdout.write(
                    self.style.NOTICE('Not overwriting file: %s' % dest))
                continue

            with open(dest, 'wb') as fp:
                fp.write(generate_key(options['length']))

            os.chmod(dest, 0o0600)
            self.stdout.write(self.style.SUCCESS('Wrote new key: %s' % dest))

        if failures:
            raise CommandError('At least one key file already exists, '
                               'not overriding.')
