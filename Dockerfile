FROM postgres:17.0

RUN  rm -rf /var/lib/postgresql/data
COPY ./load_db.sql /docker-entrypoint-initdb.d/*