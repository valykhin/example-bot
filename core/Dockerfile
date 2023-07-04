FROM docker.io/python:3.10

ARG DEBIAN_FRONTEND=noninteractive

COPY ./core /app/core
COPY ./common /app/common
WORKDIR /app/core

ENV LC_ALL='en_US.UTF-8' LANG='en_US.UTF-8' TZ=Europe/Moscow PATH=$PATH:/root/.local/bin PIPENV_PYTHON=/usr/bin/python3

RUN python3 --version && \
    pip --version && \
    pip install --user pipenv && \
    pipenv install --deploy --ignore-pipfile

CMD ["pipenv", "run", "flask", "--app", "app", "run"]