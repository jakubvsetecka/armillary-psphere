import mysql.connector
import json
import os

def get_db_connection():
    return mysql.connector.connect(
        host="database",
        user="user",
        password="password",
        database="myapp"
    )

def hlasovani_generator():
    """
    Generator yields id_hlasovani from HLASOVANI table, where LEFT_SCORE and LIB_SCORE are NOT NULL.
    """
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)  # Use buffered cursor

    try:
        query = """
        SELECT ID_HLASOVANI
        FROM HLASOVANI
        WHERE LEFT_SCORE IS NOT NULL AND LIB_SCORE IS NOT NULL
        """
        cursor.execute(query)
        for row in cursor:
            yield row[0]
    finally:
        cursor.close()
        conn.close()

def poslanec_score_generator(hlasovani_id: int):
    """
    Generator yields ID_POSLANEC, LEFT_SCORE, LIB_SCORE from POSLANEC_HLASOVANI table, where ID_HLASOVANI = hlasovani_id.
    """
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)  # Use buffered cursor

    try:
        query = """
        SELECT ID_POSLANEC, LEFT_SCORE, LIB_SCORE
        FROM POSLANEC_HLASOVANI
        WHERE ID_HLASOVANI = %s AND LEFT_SCORE IS NOT NULL AND LIB_SCORE IS NOT NULL
        """
        cursor.execute(query, (hlasovani_id,))
        for row in cursor:
            yield row
    finally:
        cursor.close()
        conn.close()


def add_to_graph(id_hlasovani, id_poslanec, left_score, lib_score):
    """
    Function that builds a graph from the projections to political compass.
    It remembers the previous scores and updates them for new hlasovani by averaging the scores.
    That means that the graph is a weighted average of all hlasovani.

    The graph is stored in a JSON file: "graph.json".

    In JSON format, the graph should look like this:
    {
        "poslanci": {
            "id_poslanec": {
                "left_score": [total_score, count],
                "lib_score": [total_score, count]
            },
            ...
        },
        "hlasovani": {
            "id_hlasovani": {
                "id_poslanec": [left_score, lib_score],
                ...
            },
            ...
        }
    }
    """

    # Check if the file exists, if not create it with an empty structure
    if not os.path.exists("graph.json"):
        with open("graph.json", "w") as file:
            json.dump({"poslanci": {}, "hlasovani": {}}, file)

    # Load the graph from the file
    with open("graph.json", "r") as file:
        graph = json.load(file)

    # Update the hlasovani part of the graph
    if id_hlasovani not in graph["hlasovani"]:
        graph["hlasovani"][id_hlasovani] = {}
    graph["hlasovani"][id_hlasovani][id_poslanec] = [left_score, lib_score]

    # Update the poslanci part of the graph
    if id_poslanec not in graph["poslanci"]:
        graph["poslanci"][id_poslanec] = {
            "left_score": [0, 0],
            "lib_score": [0, 0]
        }

    # Update left_score
    graph["poslanci"][id_poslanec]["left_score"][0] += left_score
    graph["poslanci"][id_poslanec]["left_score"][1] += 1

    # Update lib_score
    graph["poslanci"][id_poslanec]["lib_score"][0] += lib_score
    graph["poslanci"][id_poslanec]["lib_score"][1] += 1

    # Save the graph back to the file
    with open("graph.json", "w") as file:
        json.dump(graph, file)

# Usage in your main loop
for hlasovani_id in hlasovani_generator():
    for poslanec_id, left_score, lib_score in poslanec_score_generator(hlasovani_id):
        add_to_graph(str(hlasovani_id), str(poslanec_id), left_score, lib_score)
        print(f"Updated graph for hlasovani {hlasovani_id}, poslanec {poslanec_id}")