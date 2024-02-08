import pytest
from fastapi.testclient import TestClient

from tests.helpers import get_json

ORDER_IN_PAST = {
    "apt_number": "12",
    "pet_name": "dog",
    "pet_breed": "some kind",
    "start_time": "2010-01-01T12:00",
    "duration": 10,
}
ORDER_TOO_LONG = {
    "apt_number": "12",
    "pet_name": "dog",
    "pet_breed": "some kind",
    "start_time": "2030-01-01T12:00",
    "duration": 50,
}
ORDER_NEGATIVE_DURATION = {
    "apt_number": "12",
    "pet_name": "dog",
    "pet_breed": "some kind",
    "start_time": "2030-01-01T12:00",
    "duration": -5,
}
ORDER_OFF_TIME = {
    "apt_number": "12",
    "pet_name": "dog",
    "pet_breed": "some kind",
    "start_time": "2030-01-01T06:00",
    "duration": 15,
}
ORDER_NOT_ROUND = {
    "apt_number": "12",
    "pet_name": "dog",
    "pet_breed": "some kind",
    "start_time": "2030-01-01T12:05",
    "duration": 15,
}
GOOD_ORDER = {
    "apt_number": "12",
    "pet_name": "dog",
    "pet_breed": "some kind",
    "start_time": "2030-01-01T12:00",
    "duration": 15,
}


def test_no_orders(test_client: TestClient):
    response = get_json(test_client.get("/orders/2024-05-05"))
    assert response["orders"] == []


def test_order_in_past(test_client: TestClient):
    response = get_json(
        test_client.post("/orders", json=ORDER_IN_PAST), status_code=422
    )
    assert "do not book walks in the past" in response["title"]


def test_order_too_long(test_client: TestClient):
    response = get_json(
        test_client.post("/orders", json=ORDER_TOO_LONG), status_code=422
    )
    assert "Walk duration should not exceed 30 minutes" in response["title"]


def test_order_negative_duration(test_client: TestClient):
    response = get_json(
        test_client.post("/orders", json=ORDER_NEGATIVE_DURATION), status_code=422
    )
    assert "Walk duration should be greater than 0" in response["title"]


def test_order_off_time(test_client: TestClient):
    response = get_json(
        test_client.post("/orders", json=ORDER_OFF_TIME), status_code=422
    )
    assert "The walk should be booked between 7:00 and 23:00" in response["title"]


def test_order_not_round(test_client: TestClient):
    response = get_json(
        test_client.post("/orders", json=ORDER_NOT_ROUND), status_code=422
    )
    assert "Please, select strait 30 min interval for booking" in response["title"]


def test_order_occupied(test_client: TestClient):
    response1 = get_json(test_client.post("/orders", json=GOOD_ORDER))
    response2 = get_json(test_client.post("/orders", json=GOOD_ORDER))
    response3 = get_json(test_client.post("/orders", json=GOOD_ORDER), status_code=422)
    walker1 = response1["walker"]["name"]
    walker2 = response2["walker"]["name"]
    assert walker1 != walker2
    assert "No free walkers at the time" in response3["title"]
