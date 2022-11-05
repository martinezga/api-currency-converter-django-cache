FROM python:3.8.12-buster as base

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV LANG C.UTF-8

RUN pip install pipenv \
    psycopg2 \
    gunicorn

COPY Pipfile /Pipfile

RUN pipenv install --system --skip-lock

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN   groupadd -g 1000 appuser \
      && useradd --no-log-init --shell /bin/bash -u 1000 -g 1000 -o -c "" -m appuser \
      && cp -r /etc/skel/. /home/appuser \
      && chown -R 1000:1000 /home/appuser

USER appuser

FROM base as dev

CMD bin bash

FROM base as prod

COPY --chown=1000:1000 ./api ./

WORKDIR /home/appuser/api

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
CMD gunicorn --workers 4 --bind 0.0.0.0:$PORT api.configurations.wsgi:app
