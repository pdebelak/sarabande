from setuptools import setup, find_packages

setup(name='SimpleSite',
      version='0.0.1',
      description='A simple site',
      author='Peter Debelak',
      author_email='pdebelak@gmail.com',
      url='',
      packages=find_packages(),
      install_requires = [
          'flask',
          'flask-bcrypt',
          'flask-sqlalchemy',
      ]
     )
