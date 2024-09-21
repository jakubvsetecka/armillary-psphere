FROM mysql:8.0

# Copy the initialization script
COPY mysql_init/01_init.sql /docker-entrypoint-initdb.d/

RUN chmod 644 /docker-entrypoint-initdb.d/01_init.sql
RUN chown mysql:mysql /docker-entrypoint-initdb.d/01_init.sql

RUN usermod -u 1000 mysql && groupmod -g 1000 mysql
RUN chown -R mysql:mysql /var/lib/mysql /var/run/mysqld
