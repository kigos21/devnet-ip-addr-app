import pytest
from app import app, get_ip_info
from unittest.mock import patch

@pytest.fixture
def client():
    """Set up a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route."""
    with patch("app.get_ip_info") as mock_get_ip_info:
        mock_get_ip_info.return_value = {
            "ipv4": "192.168.0.1",
            "ipv6": "Not available",
            "country": "Test Country",
            "region": "Test Region",
            "city": "Test City",
            "latitude": "0.0",
            "longitude": "0.0",
            "isp": "Test ISP",
            "asn": "Test ASN",
            "country_code": "TC"
        }
        response = client.get("/")
        assert response.status_code == 200
        assert b"192.168.0.1" in response.data  # Check if IP is rendered on the page
        assert b"Test Country" in response.data  # Check if country is rendered

def test_about_route(client):
    """Test the about route."""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About" in response.data  # Check if the word "About" exists in the content

def test_get_ip_info():
    """Test the get_ip_info function with mocked API response."""
    mock_response = {
        "ip": "192.168.0.1",
        "type": "ipv4",
        "country_name": "Test Country",
        "region_name": "Test Region",
        "city": "Test City",
        "latitude": 0.0,
        "longitude": 0.0,
        "connection": {
            "isp": "Test ISP",
            "asn": "Test ASN"
        },
        "country_code": "TC"
    }
    with patch("app.requests.get") as mock_requests_get:
        mock_requests_get.return_value.json.return_value = mock_response
        ip_info = get_ip_info()

        # Validate the parsed data
        assert ip_info["ipv4"] == "192.168.0.1"
        assert ip_info["ipv6"] == "Not available"
        assert ip_info["country"] == "Test Country"
        assert ip_info["region"] == "Test Region"
        assert ip_info["city"] == "Test City"
        assert ip_info["latitude"] == 0.0
        assert ip_info["longitude"] == 0.0
        assert ip_info["isp"] == "Test ISP"
        assert ip_info["asn"] == "Test ASN"
        assert ip_info["country_code"] == "TC"
