import json, uuid, time, os, random, sqlite3
from collections import deque

def log_creator(filename):
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

    service_area = ["auth", "payment", "orders-service", "search"]

    glob_endpoint = {
            "auth" : ["/login", "/logout", "/register"],
            "payment" : ["/checkout", "/refund", "/payment-method"],
            "orders-service" : ["/orders", "/create", "/add"],
            "search" : ["/search", "/autocomplete", "/recommendation"]
        }

    workflows = {
        "place_order": [
            ("auth", "/login"),
            ("orders-service", "/create"),
            ("orders-service", "/add"),
            ("payment", "/payment-method"),
            ("payment", "/checkout")
        ],
        "login_logout": [
            ("auth", "/login"),
            ("auth", "/logout")
        ],
        "place_order_refund": [
            ("auth", "/login"),
            ("orders-service", "/create"),
            ("orders-service", "/add"),
            ("payment", "/payment-method"),
            ("payment", "/checkout"),
            ("payment", "/refund")
        ],
        "register_login_place_order": [
            ("auth", "/register"),
            ("auth", "/login"),
            ("orders-service", "/create"),
            ("orders-service", "/add"),
            ("payment", "/payment-method"),
            ("payment", "/checkout")
        ],
        "recommendation_place_order": [
            ("auth", "/login"),
            ("search", "/recommendation"),
            ("orders-service", "/create"),
            ("orders-service", "/add"),
            ("payment", "/payment-method"),
            ("payment", "/checkout")
        ]
    }

    ongoing_workflows = []

    for i in range (1000):

        action = random.choices(["new_workflow", "continue_workflow", "random_log"] 
                                ,weights = [0.3, 0.5, 0.2])[0]

        entry = {}

        if action == "new_workflow":
            wf_name = random.choice(list(workflows.keys()))
            steps = workflows[wf_name]
            event_id = generate_event_id()
            user_id = random.randint(1, 100000)

            ongoing_workflows.append({
                "steps":steps,
                "current":0,
                "event_id":event_id,
                "user_id":user_id
            })

            service_area, endpoint = steps[0]

            entries.append(generate_log_entry(service_area, endpoint, event_id))
            ongoing_workflows[-1]["current"] += 1

        elif action == "continue_workflow" and ongoing_workflows:
             # Fetch a random workflow and continue that one
             wf = random.choice(ongoing_workflows)

             if wf["current"] < len(wf["steps"]):
                service_area, endpoint = wf["steps"][wf["current"]]
                entries.append(generate_log_entry(service_area, endpoint, wf["event_id"], wf["user_id"]))
                wf["current"] += 1
            
             if wf["current"] >= len(wf["steps"]):
                ongoing_workflows.remove(wf) 
        
        else:
            # Put a random event in there:

            service_area = random.choice(list(glob_endpoint.keys()))
            endpoint = random.choice(list(glob_endpoint[service_area]))
            entries.append(generate_log_entry(service_area, endpoint))
             

    with open(f"{filename}.json", "w") as f:
        json.dump(entries, fp=f, indent=4)

def generate_time_stamp():
        curr = time.localtime(time.time())
        return time.strftime("%Y-%m-%dT%H:%M:%S", curr)

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

def generate_event_id():
    return str(uuid.uuid4())

def generate_log_entry(service_area, endpoint, event_id=None, user_id=None):
    levels = ["INFO",  "DEBUG","WARN", "ERROR", "CRITICAL"]
    level = random.choices(levels, weights=[0.60, 0.20, 0.10, 0.05, 0.05])[0]
    entry = {
        "time_stamp":generate_time_stamp(),
        "service_area":service_area,
        "endpoint":endpoint,
        "level":level,
        "response_time":generate_response_time(service_area, endpoint, level),
        "user_id":user_id if user_id else random.randint(1, 10000),
        "event_id":event_id if event_id else generate_event_id()
    }
    return entry