# Performance analyzer
import time
start_time = time.time()
# =========================

import sqlite3
import re
import datetime
# Receive a csv file
# Read csv file
# Save file into SQL databaser


def csv_to_sql(
        filepath:str,
        filename:str,
):
    """
    Reads a csv file and populate the SQL database with its data.

    Args:
        filepath(str): CSV's filepath.
        filename(str): New name given to the file received.
    """
    # SQL database connection
    connection = sqlite3.connect("database/test.db")
    cur = connection.cursor()

    # Checking if table exists
    if cur.execute("SELECT name FROM sqlite_master").fetchone() is None:
        cur.executescript("""
            CREATE TABLE test(
                    id TEXT PRIMARY KEY,
                    region TEXT,
                    origin_coord_x REAL,
                    origin_coord_y REAL,
                    dest_coord_x REAL,
                    dest_coord_y REAL,
                    datetime TEXT,
                    datasource TEXT);
            CREATE TABLE  loading_status(
                    filename TEXT,
                    status TEXT,
                    datetime TEXT
            );
                    """
                )

    # Updating status table
    date_status = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    cur.execute(f"""INSERT INTO loading_status VALUES("{filename}", "Landing_to_Database","{date_status}")""")
    
    # Opening the file in read mode
    with open(filepath,mode="r") as f:
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

    return print(f"Sucessfully uploaded {f}")



def check_upload_status(
        filename:str
)-> str:
    """
    Returns the upload status given a file name.

    Args:
        filename: Filename, same as it was used on the upload
    
    Returns:
        str: Upload Status(Landing_to_Database, Done)
    """

    # SQL database connection
    connection = sqlite3.connect("database/test.db")
    cur = connection.cursor()

    result = cur.execute(f"""SELECT status FROM loading_status WHERE filename = '{filename}' ORDER BY datetime LIMIT 1""")

    result = result.fetchall()[0][0]

    return result

# =================================
print("--- %s seconds ---" % (time.time() - start_time))