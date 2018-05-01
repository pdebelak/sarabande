import os
from setuptools import setup, find_packages, Command
import unittest


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.environ['FLASK_ENV'] = 'test'
        from sarabande import db
        db.create_all()
        suite = unittest.defaultTestLoader.discover('tests')
        runner = unittest.TextTestRunner(verbosity=1)
        return runner.run(suite)


setup(
    name='Sarabande',
    version='0.0.1',
    description='A simple blog and cms.',
    author='Peter Debelak',
    author_email='pdebelak@gmail.com',
    url='https://github.com/pdebelak/sarabande',
    packages=find_packages(),
    scripts=['scripts/create_admin', 'scripts/run_server'],
    cmdclass={'test': TestCommand},
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
        'flask-compress',
        'flask-login',
        'flask-sqlalchemy',
        'flask-wtf',
        'pillow',
        'python-slugify',
        'pyyaml',
        'uwsgi',
    ]
)
