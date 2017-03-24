import os
from setuptools import setup


setup(
    name='django-aesfield',
    version='0.4.0',
    description='Django Model Field that supports AES encryption',
    long_description=open('README.rst').read(),
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    url='https://github.com/andymckay/django-aesfield',
    include_package_data=True,
    zip_safe=False,
    packages=['aesfield',
              'aesfield/management',
              'aesfield/management/commands'],
    install_requires=[
        'Django>=1.8,<1.11',
        'm2secret-py3>=1.1'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
        ],
    )
