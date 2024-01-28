import json

import pytest
import requests
from jsonschema import validate

from python_hw_19_tests.controls import get_path

url = "https://reqres.in/api/"


def get_json_schemas(schemas_name):
    path = get_path.path(schemas_name)
    with open(path) as schemas:
        schemas = schemas.read()
    return json.loads(schemas)


def test_get_list_users():
    method_name = "users"
    params = {
        "page": 2,
        "per_page": 1
    }

    response = requests.get(url + method_name, params=params)

    response_json = response.json()
    validate(response_json, get_json_schemas("get_list_users_schemas.json"))
    assert response_json["data"][0]["id"] == 2
    assert response.status_code == 200


def test_create_user():
    method_name = "users"
    body = {
        "name": "morpheus",
        "job": "leader"
    }

    response = requests.post(url + method_name, json=body)

    response_json = response.json()
    validate(response_json, get_json_schemas("create_user_schemas.json"))
    assert response_json["name"] == body["name"]
    assert response.status_code == 201


def test_update_user_info():
    method_name = "users/2"
    body = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = requests.put(url + method_name, json=body)

    response_json = response.json()
    validate(response_json, get_json_schemas("put_user_info_schemas.json"))
    assert response_json["job"] == body["job"]
    assert response.status_code == 200


def test_delete_user():
    method_name = "users/2"


    response = requests.delete(url + method_name)

    assert response.status_code == 204
    assert response.text == ''


def test_login():
    method_name = "login"
    body = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    response = requests.post(url + method_name, json=body)

    response_json = response.json()
    validate(response_json, get_json_schemas("test_login_schemas.json"))
    assert response.status_code == 200


def test_login_without_password():
    method_name = "login"
    body = {
        "email": "eve.holt@reqres.in",
    }

    response = requests.post(url + method_name, json=body)

    assert response.status_code == 400


def test_not_found_response():
    method_name = "users/23"

    response = requests.get(url + method_name)

    assert response.status_code == 404
