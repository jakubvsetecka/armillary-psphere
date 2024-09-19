FROM mysql:8.0

RUN usermod -u 1000 mysql && groupmod -g 1000 mysql
RUN chown -R mysql:mysql /var/lib/mysql /var/run/mysqld
