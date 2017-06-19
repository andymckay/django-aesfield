import sys
import os
import codecs
from setuptools import setup, find_packages


version = '1.1'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


install_requires = [
    'Django>=1.8,<1.11',
    'm2secret-py3>=1.3'
]


test_requires = [
    'pytest==3.1.2',
    'pytest-django==3.1.2',
]


setup(
    name='django-aesfield',
    version=version,
    description='Django Model Field that supports AES encryption',
    long_description=read('README.rst'),
    author='Andy McKay',
    author_email='andym@mozilla.com',
    maintainer='Christopher Grebs',
    maintainer_email='cg@webshox.org',
    license='BSD',
    url='https://github.com/andymckay/django-aesfield',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'tests': test_requires,
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Django',
    ]
)
