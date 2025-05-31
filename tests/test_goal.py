import json

import requests
import pytest
from faker import Faker
from pytest_steps import test_steps

fake = Faker()
from modules.goal_methods import create_goal, update_goal, get_goal, delete_goal, create_goal_fixture, create_goal_from_file

from dotenv import load_dotenv
import os
load_dotenv()

my_headers = {"Authorization": os.getenv("my_token")}

def test_get_all_goals():
    result = requests.get("https://api.clickup.com/api/v2/team/90151237180/goal", headers=my_headers)
    assert result.status_code == 200
    print(result.json())


def test_create_goal():
    result, body = create_goal()
    goal_name = body["name"]
    assert result.status_code == 200
    print(result.json())
    assert result.json()["goal"]["name"] == goal_name


@test_steps("Create new goal", "Get created goal", "Update goal", "Get updated goal", "Delete goal", "Get deleted goal")
def test_crud_goal():
    result, body = create_goal()
    goal_first_name = body["name"]
    assert result.status_code == 200
    print(result.json())
    assert result.json()["goal"]["name"] == goal_first_name
    goal_id = result.json()["goal"]["id"]
    yield

    result = get_goal(goal_id)
    assert result.status_code == 200
    print(result.json())
    yield

    result, body_updated = update_goal(goal_id)
    goal_update_name = body_updated["name"]
    assert result.status_code == 200
    assert result.json()["goal"]["name"] == goal_update_name
    print(result.json())
    yield

    result = get_goal(goal_id)
    assert result.status_code == 200
    print(result.json())
    yield

    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield

    result = get_goal(goal_id)
    assert result.status_code == 404
    print(result.json())
    yield


@pytest.mark.parametrize('goal_id, status',[
                        ('null',                                 500),
                        ('90157056273',                          404),
                        ('2181229f-0cb3-4b1b-92c7-df9d831144af', 404),
                        ('d03803fb-4450-4a1c-a5af-b976c6bb8b27', 200)
])
def test_get_parameterized_list(goal_id, status):
    result = requests.get("https://api.clickup.com/api/v2/goal/" + goal_id, headers=my_headers)
    assert result.status_code == status
    print("Test passed")

@pytest.fixture()
def read_file():
  with open('test-data/goal.json', 'r') as file:
    data = json.load(file)
    data["name"] = fake.first_name()
  return data

def test_check_fixture(read_file):
    goal_response = read_file
    print(goal_response)

def test_create_goal_fixture():
    create_name = fake.first_name()
    result = create_goal_fixture(create_name)
    assert result.status_code==200

def test_create_goal_from_file(read_file):
    result = create_goal_from_file(read_file)
    assert result.status_code==200