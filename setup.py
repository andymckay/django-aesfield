import os
from setuptools import setup


setup(
    name='django-aesfield',
    version='0.1',
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
    install_requires=['M2Crypto>=0.18',
                      'Django>=1.3',
                      'm2secret>=0.1.1'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
        ],
    )
