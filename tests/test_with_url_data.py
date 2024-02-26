from src.app import calc_summaries
import requests


def get_test_data():
    url = "https://e75urw7oieiszbzws4gevjwvze0baaet.lambda-url.eu-west-2.on.aws/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def test_expected_data():
    test_data = get_test_data()
    return_json = calc_summaries(test_data)

    assert 'Sunday February 18' in return_json
    assert 'Monday February 19' in return_json
    assert 'Tuesday February 20' in return_json


def test_morning_average_temperature_calc():
    test_data = get_test_data()
    return_json = calc_summaries(test_data)

    assert return_json['Sunday February 18']["morning_average_temperature"] == '10'
