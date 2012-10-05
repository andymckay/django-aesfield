import os
import tempfile

from django.conf import settings

minimal = {
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase'
        }
    },
    'AES_KEYS': {'default': os.path.join(os.path.dirname(__file__), 'sample.key')}
}

if not settings.configured:
    settings.configure(**minimal)

from django.db import models
from django.test import TestCase

from nose.tools import eq_

from .field import AESField, EncryptedField
from .management.commands.generate_aes_keys import Command, CommandError


class TestModel(models.Model):
    key = AESField(max_length=255)


class TestBasic(TestCase):

    def test_lookup(self):
        with self.assertRaises(EncryptedField):
            TestModel.objects.filter(key='asd')

    def test_no_prefix(self):
        with self.assertRaises(ValueError):
            AESField(aes_prefix='')

    def test_get_key(self):
        key = 'some-super-secret-key'
        fn = tempfile.NamedTemporaryFile()
        fn.write(key)
        fn.flush()
        with self.settings(AES_KEYS={'default': fn.name}):
            assert AESField().get_aes_key() == 'some-super-secret-key'

    def test_generate_fails(self):
        with self.assertRaises(CommandError):
            Command().handle()

    def test_encrypt_decrypt(self):
        t = TestModel()
        f = t._meta.get_field('key')
        for k in ['foo',
                  '1234567890123456',
                  '12345678901234567',
                  u'1'.encode('ascii')]:
            eq_(k, f._decrypt(f._encrypt(k)))
