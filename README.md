# Docker and API Documentation

## Docker Commands

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

### How to get data from PSP?
Docker automatically downloads data from PSP and saves it to backend/data folder.

### How to import data to MySQL?
```
docker-compose exec backend python backend/data_import.py
```
To get rid of the data but keep the database, run:
```
docker-compose exec backend python backend/truncate_tables.py
```

### How to get embeddings?
```
curl -X POST "http://localhost:8080/embedding" --data '{"content":"some text to embed"}'
```

## API Endpoints

### 1. Get Graph Data
- **Endpoint**: `/api/data/graph`
- **Method**: GET
- **Description**: Retrieves the graph data containing hlasovani information.
- **Usage**:
  ```
  curl http://localhost:5000/api/data/graph
  ```

### 2. Get Poslanec Information
- **Endpoint**: `/api/poslanec/<int:poslanec_id>`
- **Method**: GET
- **Description**: Retrieves information about a specific poslanec by their ID.
- **Usage**:
  ```
  curl http://localhost:5000/api/poslanec/1
  ```

### 3. Get Hlasovani Information
- **Endpoint**: `/api/hlasovani/<int:hlasovani_id>`
- **Method**: GET
- **Description**: Retrieves information about a specific hlasovani by its ID.
- **Usage**:
  ```
  curl http://localhost:5000/api/hlasovani/1
  ```

## Accessing the Frontend

The React frontend is typically accessible at `http://localhost:3000` in your web browser.