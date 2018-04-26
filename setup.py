import os
from setuptools import setup, find_packages
import unittest


def run_tests():
    os.environ['SITE_ENV'] = 'test'
    import coverage
    cov = coverage.Coverage(source=['simple_site'])
    cov.start()
    discovery = unittest.defaultTestLoader.discover('tests')
    cov.stop()
    cov.report()
    return discovery


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
        'coverage',
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
