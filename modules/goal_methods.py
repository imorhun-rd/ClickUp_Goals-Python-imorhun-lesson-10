import requests
from faker import Faker
fake = Faker()

from dotenv import load_dotenv
import os
load_dotenv()

my_headers = {"Authorization": os.getenv("my_token")}

def create_goal():
    body = {
        "name": fake.first_name(),
        "description": fake.last_name()
    }
    result = requests.post("https://api.clickup.com/api/v2/team/90151115904/goal", headers=my_headers, json=body)
    return result, body


def get_goal(goal_id):
    result = requests.get("https://api.clickup.com/api/v2/goal/" + goal_id, headers=my_headers)
    return result


def update_goal(goal_id):
    update_name = fake.first_name()
    body_updated = {
        "name": update_name,
        "description": fake.last_name()
    }
    result = requests.put("https://api.clickup.com/api/v2/goal/" + goal_id, headers=my_headers, json=body_updated)
    return result, body_updated


def delete_goal(goal_id):
    result = requests.delete("https://api.clickup.com/api/v2/goal/" + goal_id, headers=my_headers)
    return result

def create_goal_fixture(param_name):
    body = {
        "name": param_name
    }
    result = requests.post("https://api.clickup.com/api/v2/team/90151115904/goal", headers=my_headers, json=body)
    return result

def create_goal_from_file(body):
    result = requests.post("https://api.clickup.com/api/v2/team/90151115904/goal", headers=my_headers, json=body)
    print(result)
    return result