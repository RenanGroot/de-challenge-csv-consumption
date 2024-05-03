# Performance analyzer
import time
start_time = time.time()
# =========================

import sqlite3
import re
# Receive a csv file
# Read csv file
# Save file into SQL databaser


def csv_to_sql(
        file:str
):
    """
    Reads a csv file and populate the SQL database with its data.

    Args:
        file(str): CSV's filepath.
    """
    # SQL database connection
    connection = sqlite3.connect("database/test.db")
    cur = connection.cursor()

    # Checking if table exists
    if cur.execute("SELECT name FROM sqlite_master").fetchone() is None:
        cur.execute("""
            CREATE TABLE test(
                    id TEXT PRIMARY KEY,
                    region TEXT,
                    origin_coord_x REAL,
                    origin_coord_y REAL,
                    dest_coord_x REAL,
                    dest_coord_y REAL,
                    datetime TEXT,
                    datasource TEXT)
                    """
                )

    # Opening the file in read mode
    with open(file,mode="r") as f:
        for row in f:
            row_s = row.split(",")

            # First row condition
            if row_s[0] == "region":
                continue
            
            # Creating variables holding the data scrapped with regex
            origin_x = re.search(r"(\d.*)(?= )",row_s[1]).group(1)
            origin_y = re.search(r"(\d+\.\d+(?=\)$))",row_s[1]).group(1)
            dest_x = re.search(r"(\d.*)(?= )",row_s[2]).group(1)
            dest_y = re.search(r"(\d+\.\d+(?=\)$))",row_s[2]).group(1)

            # Creating a Unique ID
            id = origin_x[-5:] + origin_y[-5:] + dest_y[-5:] + dest_x[-5:]

            # Inserting rows
            cur.execute(f"""
                INSERT INTO test VALUES("{id}","{row_s[0]}",{origin_x},{origin_y},{dest_x},{dest_y},"{row_s[3]}","{row_s[4]}")
                """)
            
            connection.commit()
    f.close()


csv_to_sql("samples/trips_1.csv")

# =================================
print("--- %s seconds ---" % (time.time() - start_time))