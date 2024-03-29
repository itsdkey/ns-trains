# ns-trains

* [Env file](#env-file)
* [Backend devs](#backend-devs)
  * [Local development](#local-development-and-project-conventions)
* [Start the app project using docker-compose](#start-the-app-project-using-docker-compose)
* [Doing stuff related to the project](#doing-stuff-related-to-the-project)
  * [Always execute commands inside a container](#always-execute-commands-inside-a-container)
* [Testing](#testing)
* [Debugging](#debugging)



## Env file
Env variables are used around the project. To enable working on the project locally please fill the following variables in your .env file:

* BROKER_URL=redis://redis:6379/0
* LINEMAN_DOMAIN=http://proxy:4000
* POSTGRES_USER=postgres
* POSTGRES_PASSWORD=linemen1234
* POSTGRES_DB=linemen
* POSTGRES_HOST=db
* POSTGRES_PORT=5432



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
- redis - our Broker for celery
- db - our Postgresql DB
- trains1 - the trains app
- trains2 - the trains app
- headquarters - the headquarters app
- proxy - the proxy app to act as a load balancer for the linemen replicas
- linemen - the linemen app
- migration - a shortcut to run migrations and prepopulate for the linemen service
- wdb - a python debugger for backend devs (more on that later)


### Why do we have two train services instead the same way headquarters and linemen?
The issue here is that we need to pass a ENV VAR (TRAIN_ID) to each of those services with
a different value. We could possibly use [swarm mode](https://docs.docker.com/engine/swarm/)
however because this is only for local development and to show a basic concept I decided duplicate the
service instead. More on passing unique env vars in docker compose [here](https://stackoverflow.com/questions/56203272/docker-compose-scaling-with-unique-environment-variable).

To start the application and necessary containers locally with the following:
```shell
docker compose up
```
Note: you can run this in the background just but adding the option `-d` so the command looks like:
`docker compose up -d`.

This will run all the containers. To verify it is working please check the specific container's logs like:
```shell
docker compose logs -f headquarters
```


## Doing stuff related to the project
### Always execute commands inside a container
If you want to develop with docker compose you will need sometimes to execute commands
inside the app's container because the whole environment is there. This is a separate environment from the
one you have on your computer. Entering the container is also necessary because all the env vars are loaded
from the `.env` file, and they will help you run your project smoothly.

All the commands below this paragraph will require you to enter the container first. To do that
please run one of the following commands:
```shell
docker compose run --rm trains1 bash
```
or:
```shell
docker exec -it ns-trains-1 bash
```

The first one creates a separate container if you have the project already running (it will be removed after
exiting it). The second one will enter the running container itself.

## Testing
**Please read more about tests in specific README files inside each service.**
If you are inside the container simply just run:
```shell
pytest
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
