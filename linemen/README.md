# trains

* [Backend devs](#backend-devs)
  * [Local development](#local-development-and-project-conventions)
* [Start the app project using docker-compose](#start-the-app-project-using-docker-compose)
* [Doing stuff related to the project](#doing-stuff-related-to-the-project)
  * [Always execute commands inside a container](#always-execute-commands-inside-a-container)
  * [Migrations](#migrating-and-setting-up-database)
* [Testing](#testing)
* [Debugging](#debugging)


## Backend devs
### Local development and project conventions
You are going to push commits from your local computer.
In this project we have some conventions which are installed via pre-commit.
To use them you need to create a python virtual environment:
```shell
python3.12 -m venv env/
```

Activate the env and set PYTHONPATH:
```shell
source <path_to_env>/bin/activate
```

Install the pre-commit package and necessary hooks:
```shell
pre-commit install
```

Thanks to pre-commit each commit will be checked if it's in accordance with
project's conventions. More info here: https://pre-commit.com/


## Start the app project using docker-compose
This project contains the following containers:
- app - the trains app
- tests - a shortcut to run tests in a separate container
- wdb - a python debugger for backend devs (more on that later)

To start the application and necessary containers locally with the following:
```shell
docker compose up app
```
Note: you can run this in the background just but adding the option `-d` so the command looks like:
`docker compose up -d app`.

This will run 1 container: app. Review if it is working on:
http://127.0.0.1:8000/health-check


## Doing stuff related to the project
### Always execute commands inside a container
If you want to develop with docker compose you will need sometimes to execute commands
inside the app's container because the whole environment is there. This is a separate enviroment from the
one you have on your computer. Entering the container is also necessary because all the env vars are loaded
from the `.env` file, and they will help you run your project smoothly.

All the commands below this paragraph will require you to enter the container first. To do that
please run one of the following commands:
```shell
docker compose run --rm app bash
```
or:
```shell
docker exec -it trains-app bash
```

The first one creates a separate container if you have the project already running (it will be removed after
exiting it). The second one will enter the running container itself.

### Migrating and setting up database
Migrations are provided by [Alembic](https://alembic.sqlalchemy.org/en/latest/) and
[Flask-migrate](https://flask-migrate.readthedocs.io/en/latest/). If you want to modify database,
start with changing the code in src/models. Then generate a migration file with the following command:
```shell
flask db migrate -m "Adding a new column"
```

Apply the migration with:
```shell
flask db upgrade
```

## Testing
**CAUTION!** Tests should run a separate 'clean' database. To do that please set the
`SQLALCHEMY_DATABASE_URI` correctly. After that please create an additional database with the "test_" prefix.
Tests run on a separate configuration which can be found in `src.config.TestingConfig`.

To provide tests we use a library called [pytest](https://docs.pytest.org/en/8.0.x/). Feel free to read more about it.

If you are inside the container simply just run:
```shell
pytest
```
If you are not inside the container already no worries, we got you covered. You can use a shortcut by using a separate
container that is provided in the `docker-compose.yml` called `tests`. Simply just run:
```shell
docker compose up tests
```

# Debugging
You can debug your project using a debugger. When working with docker containers it's easier to use
a debugger called [WDB](https://github.com/Kozea/wdb). It allows to debug your workflow at runtime
using a web browser. The library is already installed, so you can use it right away.

**NOTE:** Just remember about setting the 3 necessary ENV vars in your `.env` file:
* PYTHONBREAKPOINT=wdb.set_trace
* WDB_NO_BROWSER_AUTO_OPEN=1
* WDB_SOCKET_SERVER=wdb

To use it, first, place a breakpoint somewhere in the code you want to investigate:
```python
breakpoint()
```
Then start the WDB container in the background:
```shell
docker compose up -d wdb
```

After these steps run your piece of code and check the statement inside the
[interactive console](http://127.0.0.1:1984/).
