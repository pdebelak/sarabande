Sarabande
=========

A simple blog and cms. Meant to be easy to install, use, and customize.

## Usage

To use sarabande, start by cloning this repo:

```
$ git clone https://github.com/pdebelak/sarabande
```

Then install it:

```
$ cd sarabande && python3 setup.py install --user
```

Create a config file:

```
$ cp example_config.yml config.yml
```

Then edit that config file with appropriate values for you.

Create an admin:

```
$ sarabande --config config.yml setup_db
$ sarabande --config config.yml create_admin --username [your desired username] -- password [your desired password]
```

Start the server on port 5000:

```
$ sarabande --config config.yml server
```

## Development

To develop, you must have [python3](https://www.python.org/) and
[yarnpkg](https://yarnpkg.com) installed.

Install dependencies:

```
$ make setup
```

Run the server:

```
$ make server
```

Run webpack for assets:

```
$ make webpack
```

Open http://localhost:5000

You can create an admin user with:

```
$ FLASK_ENV=development venv/bin/sarabande create_admin --config example_config.ytml --username [some username] --password [some_password]
```

Then you can login and start creating pages and posts.

## License

Copyright 2018 Peter Debelak

Sarabande is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sarabande is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sarabande.  If not, see <http://www.gnu.org/licenses/>.
