# -*- coding: utf8 -*-
import os
import tempfile

from django.conf import settings
from django.db import models
from django.utils.encoding import force_bytes, force_text

import pytest

from aesfield.field import AESField, EncryptedField
from aesfield.management.commands.generate_aes_keys import (
    Command, CommandError)


class AESTestModel(models.Model):
    key = AESField(max_length=255)


class TestBasic(object):

    def test_lookup(self):
        with pytest.raises(EncryptedField):
            AESTestModel.objects.filter(key='asd')

    def test_no_prefix(self):
        with pytest.raises(ValueError):
            AESField(aes_prefix='')

    def test_get_key(self, settings):
        key = 'some-super-secret-key'
        temporary_file = tempfile.NamedTemporaryFile()
        temporary_file.write(force_bytes(key))
        temporary_file.flush()

        settings.AES_KEYS = {'default': temporary_file.name}
        assert AESField().get_aes_key() == 'some-super-secret-key'

    def test_generate_fails(self):
        with pytest.raises(CommandError):
            Command().handle()

    @pytest.mark.parametrize('key', [
        'foo', '1234567890123456', '12345678901234567',
        u'ራ'.encode('utf8'),
    ])
    def test_encrypt_decrypt(self, key):
        test_model = AESTestModel()
        field = test_model._meta.get_field('key')
        assert force_text(key) == field._decrypt(field._encrypt(key))

    def test_not_encoded(self):
        test_model = AESTestModel()
        field = test_model._meta.get_field('key')
        key = u'ራ'
        assert key == field._decrypt(field._encrypt(key))

    def test_deconstruct(self):
        test_model = AESTestModel()
        field = test_model._meta.get_field('key')
        name, path, args, kwargs = field.deconstruct()
        assert kwargs['aes_method'] == 'aesfield.default'
        assert kwargs['aes_prefix'] == 'aes:'
        assert kwargs['aes_key'] == ''
