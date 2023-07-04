FROM docker.io/python:3.10

ARG DEBIAN_FRONTEND=noninteractive

COPY ./bot /application/bot
COPY ./core /application/core
COPY ./common /application/common
WORKDIR /application/bot

ENV LC_ALL='en_US.UTF-8' LANG='en_US.UTF-8' TZ=Europe/Moscow
ENV PATH=$PATH:/root/.local/bin
ENV PIPENV_PYTHON=/usr/bin/python3

RUN python3 --version && \
    pip --version && \
    pip install --user pipenv && \
    pipenv install --deploy --ignore-pipfile && \
#    workaround for certifi conflict on venv
    pip uninstall certifi -y &&  \
    pipenv install certifi

CMD ["pipenv", "run", "python", "app.py"]