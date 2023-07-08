FROM python:3.11

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt update --no-install-recommends -y

RUN pip install poetry==1.5.1

RUN mkdir /service
WORKDIR /service

COPY poetry.lock pyproject.toml /service/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . /service/
