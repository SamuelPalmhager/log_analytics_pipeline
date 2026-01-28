import json, uuid, time, os, random, sqlite3, yaml
from collections import deque

def log_creator(filename):
    """Method for generating a single entry, start of a workflow or the continuation of a ongoing workflow. 
    Each entry should follow this following format:

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


    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

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

        action = random.choices(list(config["generator"]["action"].keys()),
                                weights = list(config["generator"]["action"].values()))[0]

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

            entries.append(generate_log_entry(service_area, endpoint, config, event_id))
            ongoing_workflows[-1]["current"] += 1

        elif action == "continue_workflow" and ongoing_workflows:
             # Fetch a random workflow and continue that one
             wf = random.choice(ongoing_workflows)

             if wf["current"] < len(wf["steps"]):
                service_area, endpoint = wf["steps"][wf["current"]]
                entries.append(generate_log_entry(service_area, endpoint, config, wf["event_id"], wf["user_id"]))
                wf["current"] += 1
            
             if wf["current"] >= len(wf["steps"]):
                ongoing_workflows.remove(wf) 
        
        else:
            # Put a random event in there:

            service_area = random.choice(list(glob_endpoint.keys()))
            endpoint = random.choice(list(glob_endpoint[service_area]))
            entries.append(generate_log_entry(service_area, endpoint, config=config))
             
    with open(f"db/{filename}.json", "w") as f:
        json.dump(entries, fp=f, indent=4)

def generate_time_stamp():
        curr = time.localtime(time.time())
        return time.strftime("%Y-%m-%dT%H:%M:%S", curr)

def generate_response_time(service_area: str , endpoint: str, level: str, config) -> float:
    """Function to sort of accurately generate response time depending on entry specifics."""

    ranges = config["generator"]["services"][service_area]["endpoints"][endpoint]
    r_min, r_max = ranges

    response_time = int(random.uniform(r_min, r_max))

    response_time = response_time * config["generator"]["log_levels"][level]

    return round(response_time, 2)

def generate_event_id():
    return str(uuid.uuid4())

def generate_log_entry(service_area, endpoint, config, event_id=None, user_id=None):
    levels = list(config["generator"]["log_levels"].keys())
    level = random.choices(levels, weights=[0.60, 0.20, 0.10, 0.05, 0.05])[0]
    entry = {
        "time_stamp":generate_time_stamp(),
        "service_area":service_area,
        "endpoint":endpoint,
        "level":level,
        "response_time":generate_response_time(service_area, endpoint, level, config=config),
        "user_id":user_id if user_id else random.randint(1, 10000),
        "event_id":event_id if event_id else generate_event_id()
    }
    return entry