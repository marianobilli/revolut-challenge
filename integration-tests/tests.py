import pytest
import requests
import urllib3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

pytest_plugins = ["docker_compose"]

@pytest.fixture(scope="session")
def wait_for_api(session_scoped_container_getter):
    urllib3.disable_warnings()
    request_session = requests.Session()    
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500])
    request_session.mount('https://', HTTPAdapter(max_retries=retries))

    session_scoped_container_getter.get("revolut_db").network_info[0]
    api_url = "https://localhost:9000/hello/status" 
    assert request_session.get(api_url, verify=False)
    return request_session

def test_health(wait_for_api):
    urllib3.disable_warnings()
    response = requests.get("https://localhost:9000/health", verify=False)
    assert response.status_code == 200

def test_status(wait_for_api):
    urllib3.disable_warnings()
    response = requests.get("https://localhost:9000/hello/status", verify=False)
    assert response.status_code == 200

def test_put_user(wait_for_api):
    urllib3.disable_warnings()
    response = requests.put("https://localhost:9000/hello/usertest", verify=False, data='{"dateOfBirth": "1980-01-01"}', headers={"Content-Type": "application/json"})
    assert response.status_code == 204

def test_duplicated_user(wait_for_api):
    urllib3.disable_warnings()
    response = requests.put("https://localhost:9000/hello/usertest", verify=False, data='{"dateOfBirth": "1980-01-01"}', headers={"Content-Type": "application/json"})
    assert response.status_code == 500

def test_get_user(wait_for_api):
    urllib3.disable_warnings()
    response = requests.get("https://localhost:9000/hello/usertest", verify=False)
    assert response.status_code == 200

def test_put_wrong_dateOfBirth_field(wait_for_api):
    urllib3.disable_warnings()
    response = requests.put("https://localhost:9000/hello/usertest", verify=False, data='{"dateOfBirthBlah": "1980-01-01"}', headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_put_wrong_date_format(wait_for_api):
    urllib3.disable_warnings()
    response = requests.put("https://localhost:9000/hello/usertest", verify=False, data='{"dateOfBirth": "01 Jan 1980"}', headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_put_long_username(wait_for_api):
    urllib3.disable_warnings()
    response = requests.put("https://localhost:9000/hello/12345678901234567890123456", verify=False, data='{"dateOfBirthBlah": "1980-01-01"}', headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_put_not_json(wait_for_api):
    urllib3.disable_warnings()
    response = requests.put("https://localhost:9000/hello/usertest", verify=False, data='"dateOfBirthBlah": "1980-01-01"', headers={"Content-Type": "application/json"})
    assert response.status_code == 400
