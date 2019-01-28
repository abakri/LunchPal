# Chow
Grab lunch with a stranger!

# Prerequisites
- virtualenv (`pip3 install virtualenv`)
- postgresql (`brew install postgres`)
- install Postman `https://www.getpostman.com/`
- install Postico `https://eggerapps.at/postico/`

# Set Up
1. clone the repository
2. create the virtual environment with `python3 -m venv venv`
3. activate the virtual environment with `source venv/bin/activate`
4. install the dependencies with `pip install -r requirements.txt`
5. make sure that postgres service is running `pg_ctl -D /usr/local/var/postgres start && brew services start postgresql`
6. configure postgres database
  1. `psql postgres`
  2. `#CREATE ROLE lunchpal WITH LOGIN PASSWORD 'lunchpal';`
  3. `#ALTER ROLE lunchpal CREATEDB;`
  4. `#\q` (quit out of psql)
  5. `psql postgres -U lunchpal` (log in as lunchpal)
  6. `#CREATE DATABASE lunchpaldb;`
  7. `#GRANT ALL PRIVILEGES ON DATABASE lunchpaldb TO lunchpal;`
  8. `#\connect lunchpaldb`
  9. `#\q`
7. initialize the database
  1. `flask db init`
  2. `flask db migrate`
  3. `python3`
  4. `from app import db`
  5. `db.create_all()`

# Development Tips
- If using vscode, install `pip install pylint-flask`, and add `"python.linting.pylintArgs": ["--load-plugins", "pylint_flask"]` to settings.json to remove any linting issues with SqlAlchemy
- Post requests to the API must have a mimetype set to json/applications

# Further Documentation
1. Flask-User (`https://flask-user.readthedocs.io/en/latest/introduction.html`)
