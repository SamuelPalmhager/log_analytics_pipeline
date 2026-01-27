import json
import time
import os
import random
import sqlite3

def log_creator():
    """Method for generating a single entry. Each entry should follow this following format:

    {
     "timestamp":"2026-01-26T10:55:46",
     "service":"auth",
     "level":"ERROR",
     "endpoint":"/login",
     "response_time_ms":842,
     "user_id":1931
    }

    This should generate 1000 entries of this and store into json file.
    """

    entries = []
    for _ in range (1000):
        entry = {}
        service_area = ["auth", "payment", "orders-service", "search"]
        levels = ["INFO", "INFO", "INFO", "INFO", "DEBUG", "DEBUG",  "DEBUG", "WARN", "WARN", "ERROR", "ERROR", "CRITICAL"]

        endpoint = {
            "auth" : ["/login", "/logout", "/register"],
            "payment" : ["/checkout", "/refund", "/payment-method"],
            "orders-service" : ["/orders", "/create", "/add"],
            "search" : ["/search", "/autocomplete", "/recommendation"]
        }

        # Create a dictionary and create a key - value pair for each line in the entry. 

        # Time entry creation, follows this format year-month-dayThour:min:secs
       
        entry["timestamp"] = generate_time_stamp()

        # Creation of service entry
        entry["service_area"] = random.choice(service_area)

        # Creation of specific endpoint
        current_endpoint_specific = random.choice(endpoint[entry["service_area"]])
        entry["endpoint"] = current_endpoint_specific

        # Creation of the level 
        entry["level"] = random.choice(levels)

        # Creation of response time 
        entry["response_time_ms"] = generate_response_time(entry["service_area"], entry["endpoint"], entry["level"])
        entries.append(entry)

    with open("order_log.json", "w") as f:
        json.dump(entries, fp=f, indent=4)

def generate_time_stamp():
        curr = time.localtime(time.time())
        year = str(curr.tm_year)
        mon = str(curr.tm_mon)
        day = str(curr.tm_mday)
        hour = str(curr.tm_hour)
        min = str(curr.tm_min)
        secs = str(curr.tm_sec)

        return year + "-" + mon + "-"+ day + "T" + hour + ":" + min + ":" + (secs if len(secs) > 1 else ("0" + secs))

def generate_response_time(service_area: str , endpoint: str, level: str) -> float:
    """Function to sort of accurately generate response time depending on entry specifics."""
    base_ranges = {

        "auth" : {
            "/login":(50, 250),
            "/logout":(30, 100),
            "/register":(80, 300)
        },

        "payment" : {
            "/checkout":(400, 900),
            "/refund":(400, 1200),
            "/payment-method":(200, 700)
        },

        "orders-service" : {
            "/orders":(100, 300),
            "/create":(50, 200),
            "/add":(50, 750)
        },

        "search" : {
            "/search":(100, 1000),
            "/autocomplete":(20, 120),
            "/recommendation":(750, 1500)
        }
    }

    level_multiplier = {
        "INFO":1.0,
        "DEBUG":1.2,
        "WARN":1.5,
        "ERROR":2.0,
        "CRITICAL":3.0
    }

    response_time = int(random.uniform(base_ranges[service_area][endpoint][0], base_ranges[service_area][endpoint][1]))

    response_time = response_time * level_multiplier[level]

    return round(response_time, 2)


log_creator()