FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN groupadd -r django \
    && useradd -r -g django django

# Debian package dependencies
RUN apt-get update
RUN apt-get install -y \
  libxml2-dev \
  libxmlsec1-dev \
  libxmlsec1-openssl \
  xmlsec1

# Python Requirements
RUN pip install --upgrade pip
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/dev.txt \
    && rm -rf /requirements

# Entry script
COPY ./compose/common/entrypoint.sh /entrypoint.sh
# Web server script
COPY ./compose/common/gunicorn.sh /gunicorn.sh

# Permissions
RUN chmod a+x /entrypoint.sh \
  /gunicorn.sh
RUN chown django /entrypoint.sh \
  /gunicorn.sh

# Django app
COPY . /app
RUN chown -R django /app
USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
