#!/bin/bash

if [ ! -d "/app/data" ]; then
    mkdir -p /app/data
    cd /app/data

    wget https://www.psp.cz/eknih/cdrom/opendata/poslanci.zip
    wget https://www.psp.cz/eknih/cdrom/opendata/hl-2021ps.zip
    wget https://www.psp.cz/eknih/cdrom/opendata/tisky.zip

    unzip poslanci.zip -d poslanci_a_osoby
    unzip hl-2021ps.zip -d 2021hl
    unzip tisky.zip -d snemovni_tisky

    rm poslanci.zip hl-2021ps.zip tisky.zip
else
    echo "Data directory already exists. Skipping download."
fi
