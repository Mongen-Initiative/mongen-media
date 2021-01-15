

# Mongen Media Service

This service is intended to manage media data for Mongen clients and services

# Start Service

In order to start this service just run:

```
docker-compose up
```

Then there are three main endpoint to use this service:

- POST `/api/v1/send_file/`

Which just receives a file thought a FormData payload, which is stored into the database.

- GET `/api/v1/get_file/<int:media_id>`

Which receives a media id, and then response with a content type that is depending on the file type.

- DELETE `/api/v1/delete_media_days_old`

Read a payload with the value `days` then deletes media that is older than the amount of days requested.

## Local development

Its highly recommended to use **[autoenv](https://github.com/inishchith/autoenv)** which will load the environment variables from the `.env` file, 
this is done each time you open Mongen Media Service folder

To install it just run `pip install autoenv` and add `` source `which activate.sh` `` to your `~/.bashrc` or `~/.bash_profile`

```
echo "source `which activate.sh`" >> ~/.bashrc
OR
echo "source `which activate.sh`" >> ~/.bash_profile
```

Then reload your shell

```
source ~/.bashrc
OR
source ~/.bash_profile
```

To develop locally, create a virtual environment and install your dependencies:

```
pip install virtualenv
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

Then, run your app:

```
python app.py
 * Running on http://localhost:9090/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

Navigate to [localhost:9090](http://localhost:9090) to see your service running locally.

## Database management

The Media service uses PosgreSQL as the database to persist all the data

SQLAlchemy is a ORM toolkit which is used to access the data on the database, more info about it can be found here https://www.tutorialspoint.com/sqlalchemy/index.htm

Finally, a migration tool called Alembic is used to maintain and track changes on  the schema https://pypi.org/project/alembic/

### Accesing the database

The best way to run the database is to run the image already incorporated in Docker Compose in Delta Reporter main repo.

`docker start mongen_media_database`

Thats will start PosgreSQL on you local port `5433`, you can connect to it directly using psql:

`psql -h localhost -p 5433 -U mongen mongen_media_db`


### Loading schema and default values

After the database is up and running, use alembic to restore the schema

`python manage.py db upgrade`

This command runs the scripts located in `migrations/versions/` in order to apply the changes on the database

If for any reason you want to restore the schema to a previous state, use `python manage.py db downgrade`
