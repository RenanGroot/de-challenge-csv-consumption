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
    connection = sqlite3.connect("database/trips.db")
    cur = connection.cursor()

    # Checking if table exists
    if cur.execute("SELECT name FROM sqlite_master").fetchone() is None:
        cur.executescript("""
            CREATE TABLE trips(
                    id TEXT PRIMARY KEY,
                    region TEXT,
                    origin_lat REAL,
                    origin_long REAL,
                    dest_lat REAL,
                    dest_long REAL,
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
    cur.execute(f"""INSERT INTO loading_status 
                VALUES("{filename}",
                  "Landing_to_Database",
                  "{date_status}")""")
    
    # Opening the file in read mode
    with open(filepath,mode="r") as f:
        for row in f:
            row_s = row.split(",")

            # First row condition
            if row_s[0] == "region":
                continue
            
            # Creating variables holding the data scrapped with regex
            origin_lat = re.search(r"(\d.*)(?= )",row_s[1]).group(1)
            origin_long = re.search(r"(\d+\.\d+(?=\)$))",row_s[1]).group(1)
            dest_lat = re.search(r"(\d.*)(?= )",row_s[2]).group(1)
            dest_lat = re.search(r"(\d+\.\d+(?=\)$))",row_s[2]).group(1)

            # Creating a Unique ID
            id = origin_lat[-5:] + origin_long[-5:] + dest_lat[-5:] + dest_lat[-5:] + row_s[3][:10]

            try:
                # Inserting rows
                cur.execute(f"""
                    INSERT INTO trips 
                            VALUES("{id}",
                            "{row_s[0]}",
                            {origin_lat},
                            {origin_long},
                            {dest_lat},
                            {dest_lat},
                            "{row_s[3]}",
                            "{row_s[4]}")
                    """)
            except:
                continue
    f.close()

    # Updating status table
    date_status = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    cur.execute(f"""INSERT INTO loading_status 
                VALUES("{filename}", 
                "Finished",
                "{date_status}"
                )""")

    connection.commit()
    return print(f"Sucessfully uploaded {filename}")



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
    connection = sqlite3.connect("database/trips.db")
    cur = connection.cursor()

    result = cur.execute(f"""SELECT status 
                         FROM loading_status 
                         WHERE filename = '{filename}' 
                         ORDER BY datetime DESC LIMIT 1""")

    result = result.fetchall()[0][0]

    return result

def weekly_avg_reg(
        region:str
) -> float:
    """
    Gives the weekly average number of trips for an area defined by a region.

    Args:
        region(str): Target region.

    Returns:
        float: Weekly average trips.
    """

    # SQL database connection
    connection = sqlite3.connect("database/trips.db")
    cur = connection.cursor()

    result = cur.execute(f""" SELECT AVG(trips_count) 
                FROM 
                        (select 
                        region,
                        strftime('%W', datetime) WeekNumber,
                        MAX(DATE(datetime, 'weekday 0', '-7 day')) WeekStart,
                        MAX(DATE(datetime, 'weekday 0', '-1 day')) WeekEnd,
                        COUNT(*) as trips_count
                        FROM trips
                        WHERE region = '{region}'
                        GROUP BY WeekNumber, region)
                GROUP BY region;
                """)
    
    result = result.fetchall()[0][0]

    return result

# =================================
print("--- %s seconds ---" % (time.time() - start_time))

