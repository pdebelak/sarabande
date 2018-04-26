import os
from setuptools import setup, find_packages
import unittest


def run_tests():
    os.environ['SITE_ENV'] = 'test'
    return unittest.defaultTestLoader.discover('tests')


setup(
    name='SimpleSite',
    version='0.0.1',
    description='A simple site',
    author='Peter Debelak',
    author_email='pdebelak@gmail.com',
    url='',
    packages=find_packages(),
    test_suite='setup.run_tests',
    extras_require={
        'dev': [
            'faker',
        ]
    },
    tests_require=[
        'faker',
    ],
    install_requires=[
        'flask',
        'flask-bcrypt',
        'flask-sqlalchemy',
        'flask-wtf',
        'flask-bcrypt',
        'flask-login',
        'pyyaml',
        'python-slugify',
    ]
)
