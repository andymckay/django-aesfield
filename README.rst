AES Field
=============

Provides an AES field for Django that does AES encryption and decryption
using `m2secret-py3`_, a Python wrapper for OpenSSL.

.. _M2Crypto: https://pypi.python.org/pypi/m2secret-py3

Usage
-----

Like any other field::

    from aesfield.field import AESField

    class SomeModel(...):
        key = AESField()

Configuration
-------------

AESField takes the following parameters beyond a normal CharField:

* `aes_prefix`: the prefix to use on fields, defaults to `aes:`

* `aes_key`: the key to use in the lookup method to find a suitable key for
  this field, defaults to `default`

Settings:

* `AES_METHOD`: the module to look in for a key lookup method, if you want
  something different from the default, `aesfield.default`

* `AES_KEYS`: used by the `aesfield.default` method. It's a dictionary of keys
  to filenames. Those files must be able to be read by the Django process. It
  must have a `default` key, unless you specify a specifc one in `aes_key`

Commands
--------

If you add `aesfield` to `INSTALLED_APPS` you'll get one more command,
`generate_aes_keys`. This will generate a new file for each file mentioned in
the `AES_KEYS` dictionary. *But only if that file does not already exist*.
