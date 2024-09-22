FROM --platform=linux/amd64 python:3.9

WORKDIR /app

# Install wget and unzip
RUN apt-get update && apt-get install -y wget unzip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/download_and_process_data.sh

ENTRYPOINT ["/bin/bash", "-c", "/app/download_and_process_data.sh && flask run --host=0.0.0.0"]

EXPOSE 5000
