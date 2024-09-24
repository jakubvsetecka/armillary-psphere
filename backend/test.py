import requests
import json
import numpy as np

from bs4 import BeautifulSoup
import re

import mysql.connector
from typing import Generator, Tuple, List

def get_embedding(content):
    url = "http://localhost:8080/embedding"
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
    diff_vectors = [left - right for left, right in zip(left_embeddings, right_embeddings)]

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

def get_full_law_text(url):
    response = requests.get(url)

    # Parse the XML content
    soup = BeautifulSoup(response.text, 'xml')

    # Find the div with id 'main-content'
    main_content = soup.find('div', {'id': 'main-content'})

    if main_content:
        # Extract all text from the main content
        full_text = main_content.get_text(separator=' ', strip=True)

        # Remove extra whitespace
        full_text = re.sub(r'\s+', ' ', full_text).strip()

        # Remove any remaining HTML entities
        full_text = re.sub(r'&[a-zA-Z]+;', '', full_text)

        return full_text
    else:
        return "Could not find the main-content div"

def get_scores_for_law(url, leftism_vector, libertarian_vector):
    full_law_text = get_full_law_text(url)

    # Calculate scores
    leftism_score = calculate_score(full_law_text, leftism_vector)
    libertarian_score = calculate_score(full_law_text, libertarian_vector)

    return leftism_score, libertarian_score

def get_db_connection():
    return mysql.connector.connect(
        host="database",
        user="user",
        password="password",
        database="myapp"
    )

def hlasovani_url_generator() -> Generator[Tuple[int, str], None, None]:
    """
    Generator that yields ID_HLASOVANI and URL_TISK connected through the HIST table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT h.ID_HLASOVANI, t.URL_TISK
        FROM HLASOVANI h
        JOIN HIST hi ON h.ID_HLASOVANI = hi.ID_HLASOVANI
        JOIN TISKY t ON hi.ID_TISK = t.ID_TISK
        """
        cursor.execute(query)

        for (id_hlasovani, url_tisk) in cursor:
            yield (id_hlasovani, url_tisk)

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


if __name__ == "__main__":
    # leftism_vector, libertarian_vector = get_vectors()

    for hlasovani_id, url_tisk in hlasovani_url_generator():
        if url_tisk != "":
            print(f"URL: {url_tisk}")
        # print(f"Hlasovani ID: {hlasovani_id}, URL: {url_tisk}")
    #leftism_score, libertarian_score = get_scores_for_law(url, leftism_vector, libertarian_vector)
