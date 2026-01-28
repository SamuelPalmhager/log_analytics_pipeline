import sqlite3

def perform_analysis(filename):

    conn = sqlite3.connect(f"db/{filename}.db")
    conn.row_factory = sqlite3.Row

    # For retrieving the top 20 users ordered by their average latency, must have 3 or more entries to be analysed
    cur = conn.execute("SELECT user_id , AVG(response_time) AS avg_latency, COUNT(*) AS hits " \
    "FROM order_logs " \
    "GROUP BY user_id " \
    "HAVING COUNT(*) >= 3 "
    "ORDER BY avg_latency DESC " \
    "LIMIT 20")

    rows = cur.fetchall()
    for r in rows:
        print(dict(r))

    cur = conn.execute( 
    "SELECT service_area, " \
    "SUM(CASE WHEN level = 'INFO' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS error_rate " \
    "FROM order_logs " \
    "GROUP BY service_area")

    rows = cur.fetchall()
    for r in rows: 
        print(dict(r))

    conn.close()
    return rows

#if __name__ == "__main__":
#    analytics("logs")