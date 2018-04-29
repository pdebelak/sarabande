import os
from setuptools import setup, find_packages
import unittest


def run_tests():
    os.environ['FLASK_ENV'] = 'test'
    from simple_site import db
    db.create_all()
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
    scripts=['scripts/create_admin'],
    extras_require={
        'dev': [
            'faker',
            'coverage',
        ]
    },
    tests_require=[
        'faker',
        'coverage',
    ],
    install_requires=[
        'flask',
        'flask-bcrypt',
        'flask-sqlalchemy',
        'flask-wtf',
        'flask-bcrypt',
        'flask-login',
        'flask-compress',
        'pyyaml',
        'python-slugify',
    ]
)
