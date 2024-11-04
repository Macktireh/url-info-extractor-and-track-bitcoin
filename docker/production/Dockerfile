ARG PYTHON_BASE=3.12-slim

FROM python:$PYTHON_BASE AS builder

# set work directory
WORKDIR /project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/project/src

# install python dependencies
COPY ./requirements/base.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project files to container
COPY src/ src/

# collect static files
RUN python src/manage.py collectstatic --noinput

EXPOSE 8000

CMD [ "gunicorn", "src.config.wsgi:application", "--bind", "0.0.0.0:8000", "--log-level", "info" ]
