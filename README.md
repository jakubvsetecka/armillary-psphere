### How to start a Docker Composer?
```
docker-compose build
docker-compose up [-d]
```
> Use -d to run Docker in the background

or

```
docker-compose up --build
```
to build and run

### How to connect to MySQL server?
```
docker-compose exec database mysql -uuser -ppassword myapp
```

### Is it not working?
```
docker-compose logs backend
docker-compose logs frontend
docker-compose logs database
```

### How to turn it off?
```
docker-compose down
```
or `Ctrl + C`
