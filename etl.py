import sqlite3
import json

def etl():
    """ ETL stands for 'extract load transform' and makes sure that unstructured or incomplete data
     gets treated and structured for loading into a sql-based database.  
     
     This function will extract the contents of order_log.json, perform some form of cleaning, and then load it into a local sqlite .log file. """
    
    conn = sqlite3.connect('logs.db')

    conn.execute("CREATE TABLE order_logs ("
        "time_stamp varchar(255), "
        "service_area varchar(255),"
        "endpoint varchar(255),"
        "level varchar(255),"
        "response_time float,"
        "user_id integer,"
        "event_id varchar(255))")

    with open("order_log.json", 'r') as f:
        data = json.load(f)
    
    for item in data:
        conn.execute("INSERT INTO order_logs (time_stamp, service_area, endpoint, level, response_time, user_id, event_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (item["time_stamp"], item["service_area"], item["endpoint"], item["level"], item["response_time"], item["user_id"], item["event_id"]))
        
    conn.commit()
    conn.close()

etl()