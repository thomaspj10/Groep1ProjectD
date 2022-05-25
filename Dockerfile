FROM python:3.9-slim

RUN apt-get update 

# Installs tkinter, needed for python
RUN apt-get -y install tk tcl

RUN pip install --upgrade cython
RUN pip install --upgrade pip

# Installs geckodriver, needed for pdf downloading
RUN  apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
    && rm -fr /var/lib/apt/lists/*                \
    && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
    && apt-get purge -y ca-certificates curl

# Creates and sets the working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Installs all python/pip dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Setting PYTHONUNBUFFERED to a non empty value ensures that the python output is sent straight to terminal
# Which allows you to view the python ouput in the container log, `docker logs CONTAINERNAME`
ENV PYTHONUNBUFFERED 1 

COPY . . 