import mysql.connector
import csv
import os
import re
from datetime import datetime

PATH = "data"

def convert_date(date_str):
    return datetime.strptime(date_str, '%d.%m.%Y').strftime('%Y-%m-%d')

# Connect to the database
conn = mysql.connector.connect(
    host="database",
    user="user",
    password="password",
    database="myapp"
)
cursor = conn.cursor()

# Disable foreign key checks
cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

def import_hlasovani():
    print("Importing hlasovani data...")
    dirs_hl = [x for x in os.listdir(PATH) if x.endswith("hl")]
    for dir in dirs_hl:
        filename = [x for x in os.listdir(os.path.join(PATH, dir)) if x.endswith("s.unl")][0]
        file_path = os.path.join(PATH, dir, filename)
        print(f"Processing {file_path}")
        with open(file_path, 'r', encoding='windows-1250') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                try:
                    converted_date = convert_date(row[5])
                    cursor.execute("INSERT INTO hlasovani (ID_HLASOVANI, VYSLEDEK_HLASOVANI, NAZEV_HLASOVANI, DATUM_HLASOVANI) VALUES (%s, %s, %s, %s)",
                              (row[0], row[-4], row[-3], converted_date))
                except Exception as e:
                    print(f"Error processing hlasovani row: {row}")
                    print(f"Error message: {str(e)}")
    conn.commit()

def import_osoba():
    print("Importing osoba data...")
    osoba_file = os.path.join(PATH, "poslanci_a_osoby", "osoby.unl")
    with open(osoba_file, 'r', encoding='windows-1250') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            try:
                cursor.execute("INSERT INTO osoba (ID_OSOBA, JMENO_OSOBA, PRIJMENI_OSOBA) VALUES (%s, %s, %s)",
                          (row[0], row[3], row[2]))
            except Exception as e:
                print(f"Error processing osoba row: {row}")
                print(f"Error message: {str(e)}")
    conn.commit()

def import_poslanec():
    print("Importing poslanec data...")
    poslanec_file = os.path.join(PATH, "poslanci_a_osoby", "poslanec.unl")
    with open(poslanec_file, 'r', encoding='windows-1250') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            try:
                cursor.execute("INSERT INTO poslanec (ID_POSLANEC, ID_OSOBA) VALUES (%s, %s)",
                          (row[0], row[1]))
            except Exception as e:
                print(f"Error processing poslanec row: {row}")
                print(f"Error message: {str(e)}")
    conn.commit()

def import_poslanec_hlasovani():
    max_allowed_rows = 100000
    print("Importing poslanec_hlasovani data...")
    dirs_hl = [x for x in os.listdir(PATH) if x.endswith("hl")]
    for dir in dirs_hl:
        filenames = [filename for filename in os.listdir(os.path.join(PATH, dir)) if re.search(r'hl.{4}h.{1}.unl', filename)]
        for filename in filenames:
            file_path = os.path.join(PATH, dir, filename)
            print(f"Processing {file_path}")
            with open(file_path, 'r', encoding='windows-1250', errors='ignore') as f:
                reader = csv.reader(f, delimiter='|')
                for row in reader:
                    max_allowed_rows -= 1
                    if max_allowed_rows == 0:
                        break
                    try:
                        cursor.execute("INSERT INTO poslanec_hlasovani (ID_POSLANEC, ID_HLASOVANI, VYSLEDEK) VALUES (%s, %s, %s)",
                                (row[0], row[1], row[2]))
                    except Exception as e:
                        print(f"Error processing poslanec_hlasovani row: {row}")
                        print(f"Error message: {str(e)}")
            conn.commit()

def import_tisky():
    print("Importing tisky data...")
    tisky_file = os.path.join(PATH, "snemovni_tisky", "tisky.unl")
    with open(tisky_file, 'r', encoding='windows-1250', errors='ignore') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            try:
                druh_tisk = int(row[1])
                if druh_tisk in (1, 2):
                    cursor.execute("INSERT INTO tisky (ID_TISK, DRUH_TISK, NAZEV_TISK, URL_TISK) VALUES (%s, %s, %s, %s)",
                              (row[0], druh_tisk, row[15], row[19]))
            except Exception as e:
                print(f"Error processing tisky row: {row}")
                print(f"Error message: {str(e)}")
    conn.commit()

def import_hist():
    print("Importing hist data...")
    hist_file = os.path.join(PATH, "snemovni_tisky", "hist.unl")
    with open(hist_file, 'r', encoding='windows-1250', errors='ignore') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            try:
                if row[3]:
                    cursor.execute("INSERT INTO hist (ID_HIST, ID_TISK, ID_HLASOVANI) VALUES (%s, %s, %s)",
                            (row[0], row[1], row[3]))
            except Exception as e:
                print(f"Error processing hist row: {row}")
                print(f"Error message: {str(e)}")
    conn.commit()

# Main execution
try:
    import_hlasovani()
    import_osoba()
    import_poslanec()
    import_poslanec_hlasovani()
    import_tisky()
    import_hist()
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    conn.commit()
    conn.close()

print("Import process completed.")
