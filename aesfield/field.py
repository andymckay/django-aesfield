from importlib import import_module

from django.conf import settings
from django.db import models
from django.db.migrations.writer import SettingsReference
from django.utils.encoding import smart_bytes, smart_text

from m2secret import Secret


class EncryptedField(Exception):
    pass


class AESField(models.TextField):
    description = 'A field that uses AES encryption.'

    def __init__(self, *args, **kwargs):
        self.aes_prefix = kwargs.pop('aes_prefix', 'aes:')
        if not self.aes_prefix:
            raise ValueError('AES Prefix cannot be null.')
        self.aes_method = kwargs.pop(
            'aes_method', getattr(settings, 'AES_METHOD', 'aesfield.default'))
        self.aes_key = kwargs.pop('aes_key', '')
        super(AESField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(AESField, self).deconstruct()
        kwargs['aes_method'] = SettingsReference(self.aes_method, 'AES_METHOD')
        kwargs['aes_prefix'] = self.aes_prefix
        kwargs['aes_key'] = self.aes_key
        return name, path, args, kwargs

    def get_aes_key(self):
        result = import_module(self.aes_method).lookup(self.aes_key)
        if len(result) < 10:
            raise ValueError('Passphrase cannot be less than 10 chars.')
        return result

    def _no_lookup(self, *args, **kwargs):
        raise EncryptedField('You cannot do lookups on an encrypted field.')

    get_db_prep_lookup = get_prep_lookup = get_lookup = _no_lookup

    def from_db_value(self, value, expression, connection, context):
        if not value or not value.startswith(self.aes_prefix):
            return value
        return self._decrypt(value[len(self.aes_prefix):])

    def to_python(self, value):
        if not value or not value.startswith(self.aes_prefix):
            return value
        return self._decrypt(value[len(self.aes_prefix):])

    def get_prep_value(self, value):
        if not value:
            return value

        return self.aes_prefix + self._encrypt(value)

    def _encrypt(self, value):
        secret = Secret()
        secret.encrypt(smart_bytes(value), self.get_aes_key())
        return secret.serialize()

    def _decrypt(self, value):
        secret = Secret()
        secret.deserialize(value)
        return smart_text(secret.decrypt(self.get_aes_key()))
