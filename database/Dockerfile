#FROM postgres:latest
FROM postgis/postgis
ENV POSTGRES_PASSWORD=mypass
ENV POSTGRES_USER=myuser
ENV POSTGRES_DB=mydb

COPY create_fixtures.sql /docker-entrypoint-initdb.d/create_fixtures.sql
COPY fill_tables.sql /docker-entrypoint-initdb.d/fill_tables.sql
