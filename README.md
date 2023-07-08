# build-system

![Linters](https://github.com/TimePeak/users/actions/workflows/linters.yml/badge.svg)
![Tests](https://github.com/TimePeak/users/actions/workflows/tests.yml/badge.svg)


## Run service via Docker

```shell
docker-compose up -d
```

## Run service via uvicorn

### Create and activate virtual environment

```shell
python -m virtualenv --python=3.11 venv

./venv/Scripts/activate # source ./venv/bin/activate
```



### Install dependencies

* Install poetry with command `pip install poetry`
* Install dependencies with command `poetry install`

### Install pre-commit hooks

To install pre-commit simply run inside the shell:

```shell
pre-commit install
```

To run it on all of your files, do

```shell
pre-commit run --all-files
```



### Run service

```shell
uvicorn app.main:app --reload
```

