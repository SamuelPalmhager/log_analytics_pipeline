import sqlite3
import json

def etl(filename):
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
        "event_id varchar(255)," \
        "response_bucket varchar(50))")

    with open(f"{filename}.json", 'r') as f:
        data = json.load(f)
    
    for item in data:
        conn.execute("INSERT INTO order_logs (time_stamp, service_area, endpoint, level, response_time, user_id, event_id, response_bucket) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (item["time_stamp"], 
                      item["service_area"].lower(), 
                      item["endpoint"].lower(), 
                      item["level"].upper(), 
                      item["response_time"], 
                      item["user_id"], 
                      item["event_id"],
                      derive_response_bucket(item["response_time"])))
        
    conn.commit()
    conn.close()

def derive_response_bucket(rt):
    if rt < 200: 
        return "fast"
    elif rt <= 500:
        return "normal"
    elif rt <= 800:
        return "slow"
    else:
        return "critical"
