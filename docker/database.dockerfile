FROM postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=mysecretpassword
ENV POSTGRES_DB=prod_live
EXPOSE 5432
ADD ../helpers/database_management/setup_database.sql /docker-entrypoint-initdb.d/