FROM apache/superset:5.0.0

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libldap2-dev \
       libsasl2-dev \
       libssl-dev \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN . /app/.venv/bin/activate \
    && uv pip install \
       python-ldap \
       psycopg2-binary

USER superset
