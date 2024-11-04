ARG PYTHON_BASE=3.12-slim

FROM python:$PYTHON_BASE AS builder

# set work directory
WORKDIR /project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY ./requirements/base.txt requirements.txt
RUN pip install -r requirements.txt

# copy project files to container
COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY src/ src/

ENTRYPOINT ["/entrypoint"]
