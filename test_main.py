from main import get_temperature
from unittest.mock import patch
import pytest


######## VALID TESTS #########
valid_tests = [
    (62, -14.235004, -51.92528, 16),
    (62.54, -14.235004, -51.92528, 16),
    (5, 15.58564, -13.85478, -15),
    (-13, 22.8523, 17.358746, -25),
    (0, 22.8523, 17.358746, -17),
]


@pytest.mark.parametrize("rTemperature,lat,lng,expected", valid_tests)
def test_get_temperature_by_lat_lng(rTemperature, lat, lng, expected):

    mock_get_patcher = patch('main.requests.get')
    temperature = {"currently": {"temperature": rTemperature}}

    mock_get = mock_get_patcher.start()
    mock_get.return_value.json.return_value = temperature
    response = get_temperature(lat, lng)
    mock_get_patcher.stop()

    assert response == expected


######## TESTs WITH INVALID LAT/LNG #########
invalid_lat_lng = [
    (62, 90.003453, 17.358746, {"code": 400,
                                "error": "The given location is invalid."}),
    (62, -90.003453, 17.358746, {"code": 400,
                                 "error": "The given location is invalid."}),
    (62, 32.23456, 180.358746, {"code": 400,
                                "error": "The given location is invalid."}),
    (62, 32.23456, -180.358746, {"code": 400,
                                 "error": "The given location is invalid."}),
]


@pytest.mark.parametrize("rTemperature,lat,lng,expected", invalid_lat_lng)
def test_get_temperature_with_invalid_lat_lng(rTemperature, lat, lng, expected):

    response = get_temperature(lat, lng)

    assert response == expected


######## TESTs WITH RANDOM LAT/LNG TYPE #########
invalid_lat_lng_type = [
    (62, None, 17.358746, {'code': 400, 'error': 'Poorly formatted request'}),
    (62, -90.003453, "Test", {'code': 400,
                              'error': 'Poorly formatted request'}),
]


@pytest.mark.parametrize("rTemperature,lat,lng,expected", invalid_lat_lng_type)
def test_get_temperature_with_invalid_lat_lng_type(rTemperature, lat, lng, expected):

    response = get_temperature(lat, lng)

    assert response == expected


######## TESTs WITH UNEXPECTED RETURN #########
unexpected_return = [
    (None, 89.98345, 17.358746, "Invalid type data"),
    ('Test', 15.23098, 17.358746, "Invalid type data"),
]


@pytest.mark.parametrize("rTemperature,lat,lng,expected", unexpected_return)
def test_get_temperature_with_unexpected_return(rTemperature, lat, lng, expected):
    mock_get_patcher = patch('main.requests.get')
    temperature = {"currently": {"temperature": rTemperature}}

    mock_get = mock_get_patcher.start()
    mock_get.return_value.json.return_value = temperature
    response = get_temperature(lat, lng)
    mock_get_patcher.stop()

    assert response == expected
