import requests
import json
import numpy as np

from bs4 import BeautifulSoup
import re
import io
from PyPDF2 import PdfReader

import mysql.connector
from typing import Generator, Tuple, List

def get_embedding(content):
    url = "http://llama_server:8080/embedding"
    data = {"content": content[:1000]}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers).json()["embedding"]
    except Exception as e:
        print(f"Error getting embedding for content: {content[:50]}")
        print(f"Error message: {str(e)}")
        response = None
    return response

def calculate_difference_vector(left_concepts, right_concepts):
    # Get embeddings
    left_embeddings = np.array([get_embedding(concept) for concept in left_concepts])
    right_embeddings = np.array([get_embedding(concept) for concept in right_concepts])

    # Calculate difference vectors
    try:
        diff_vectors = [left - right for left, right in zip(left_embeddings, right_embeddings)]
    except Exception as e:
        raise ValueError(f"Error calculating difference vectors: {str(e)}")

    # Average the difference vectors
    difference_vector = np.mean(diff_vectors, axis=0)

    # Normalize the vector
    difference_vector = difference_vector / np.linalg.norm(difference_vector)

    return difference_vector

def get_vectors():
    # Define left and right concepts
    left_concepts = ["leftist", "socialism", "communism"]
    right_concepts = ["rightist", "conservatism", "capitalism"]

    leftism_vector = calculate_difference_vector(left_concepts, right_concepts)

    authoritarian_concepts = [
        "Centralized power",
        "State control of media",
        "Restricted civil liberties",
        "Surveillance of citizens",
        "Censorship"
    ]
    libertarian_concepts = [
        "Individual liberty",
        "Minimal government",
        "Free markets",
        "Personal responsibility",
        "Non-interventionist foreign policy"
    ]

    libertarian_vector = calculate_difference_vector(libertarian_concepts, authoritarian_concepts)

    return leftism_vector, libertarian_vector

# Function to calculate leftism score
def calculate_score(word, vector):
    word_embedding = get_embedding(word)
    return np.dot(word_embedding, vector)

def get_scores_from_text(text, leftism_vector, libertarian_vector):

    # truncate the text to 1000 characters
    text = text[:1000]

    # Calculate scores
    leftism_score = calculate_score(text, leftism_vector)
    libertarian_score = calculate_score(text, libertarian_vector)

    return leftism_score, libertarian_score

def get_db_connection():
    return mysql.connector.connect(
        host="database",
        user="user",
        password="password",
        database="myapp"
    )

def hlasovani_tisk_generator() -> Generator[Tuple[int, int, int, int], None, None]:
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)  # Use buffered cursor

    try:
        query = """
        SELECT h.ID_HLASOVANI, t.CT_TISK, t.CISLO_ZA_TISK, t.ID_ORG_OBD
        FROM HLASOVANI h
        JOIN HIST hi ON h.ID_HLASOVANI = hi.ID_HLASOVANI
        JOIN TISKY t ON hi.ID_TISK = t.ID_TISK
        """
        cursor.execute(query)

        for (id_hlasovani, ct_tisk, cislo_za_tisk, id_org_obd) in cursor:
            print(f"Processing hlasovani_id: {id_hlasovani}")
            print(f"ct_tisk: {ct_tisk}, cislo_za_tisk: {cislo_za_tisk}, id_org_obd: {id_org_obd}")
            yield id_hlasovani, ct_tisk, cislo_za_tisk, id_org_obd
    except Exception as e:
        print(f"An error occurred in generator: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def get_poslanec_results(hlasovani_id: int) -> List[Tuple[int, str]]:
    """
    Function that takes HLASOVANI_ID and returns a list of tuples containing
    ID_POSLANEC and VYSLEDEK from the POSLANEC_HLASOVANI table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT ID_POSLANEC, VYSLEDEK
        FROM POSLANEC_HLASOVANI
        WHERE ID_HLASOVANI = %s
        """
        cursor.execute(query, (hlasovani_id,))

        return list(cursor.fetchall())

    finally:
        cursor.close()
        conn.close()

def get_url(obdobi: int, cislo_tisku: int, cisla_za: int):
    """
    Function that takes obdobi, cislo_tisku and cisla_za and returns URL
    """

    # convert obdobi identifier to obdobi
    obdobi -= 164

    return f"https://www.psp.cz/sqw/text/tiskt.sqw?O={obdobi}&CT={cislo_tisku}&CT1={cisla_za}"

def get_pdf_url(webpage_url):
    response = requests.get(webpage_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        pdf_link = soup.select_one('.document-media-attachments-x ul li.pdf a')
        if pdf_link:
            return 'https://www.psp.cz' + pdf_link['href']
    return None

def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
        return None

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_from_url(url):
    pdf_text = ""
    try:
        # Get the PDF URL
        pdf_url = get_pdf_url(url)
        if not pdf_url:
            raise ValueError("Failed to find the PDF link on the webpage.")
        print(f"Found PDF URL: {pdf_url}")

        # Download the PDF
        pdf_file = download_pdf(pdf_url)
        if not pdf_file:
            raise ValueError("Failed to download the PDF.")

        # Extract text from the PDF
        pdf_text = extract_text_from_pdf(pdf_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    print("Successfully extracted text from the PDF.")
    return pdf_text

def get_poslanci_scores(poslanci_votes, text_left_score, lib_text_score):
    """
    Function that takes a list of tuples containing ID_POSLANEC and VYSLEDEK
    and returns a list of tuples containing ID_POSLANEC and SCORE.
    """
    poslanci_scores = []
    for poslanec_id, vote in poslanci_votes:
        left_score = "nan"
        lib_score = "nan"
        if vote == "A":
            left_score = text_left_score
            lib_score = lib_text_score
        elif vote in ["B", "N"]:
            left_score = -text_left_score
            lib_score = -lib_text_score

    poslanci_scores.append((poslanec_id, (left_score, lib_score)))

    return poslanci_scores

def update_hlasovani_scores(hlasovani_id, scores):
    """
    Function that updates the hlasovani score in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        UPDATE HLASOVANI
        SET LEFT_SCORE = %s, LIB_SCORE = %s
        WHERE ID_HLASOVANI = %s
        """
        cursor.execute(query, (scores[0], scores[1], hlasovani_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def update_poslanec_hlasovani_scores(poslanec_id, hlasovani_id, scores):
    """
    Function that updates the poslanec_hlasovani score in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        UPDATE POSLANEC_HLASOVANI
        SET LEFT_SCORE = %s, LIB_SCORE = %s
        WHERE ID_POSLANEC = %s AND ID_HLASOVANI = %s
        """
        cursor.execute(query, (scores[0], scores[1], poslanec_id, hlasovani_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def run():
    leftism_vector, libertarian_vector = get_vectors()

    for idx, (hlasovani_id, ct_tisk, cislo_za_tisk, id_org_obd) in enumerate(hlasovani_tisk_generator()):
        if idx > 1:
            break

        print(f"Processing hlasovani_id: {hlasovani_id}")

        poslanec_results = get_poslanec_results(hlasovani_id)

        # get text from URL
        tisk_url = get_url(id_org_obd, ct_tisk, cislo_za_tisk)
        tisk_text = get_text_from_url(tisk_url)

        # get scores
        leftism_score, libertarian_score = get_scores_from_text(tisk_text, leftism_vector, libertarian_vector)
        poslanci_scores = get_poslanci_scores(poslanec_results, leftism_score, libertarian_score)

        # update tables with scores
        update_hlasovani_scores(hlasovani_id, (leftism_score, libertarian_score))
        for poslanec_id, scores in poslanci_scores:
            update_poslanec_hlasovani_scores(poslanec_id, hlasovani_id, scores)

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
