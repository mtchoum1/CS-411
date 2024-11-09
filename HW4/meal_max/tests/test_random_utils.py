import pytest
import requests

from meal_max.utils.random_utils import get_random

# Define the mock values
RANDOM_NUMBER = 0.45

@pytest.fixture
def mock_random_org(mocker):
    """Fixture to mock the response from random.org."""
    # Patch the requests.get call
    mock_response = mocker.Mock()
    # Set the response text to the mocked random number as a string
    mock_response.text = f"{RANDOM_NUMBER}"
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response

def test_get_random(mock_random_org):
    """Test retrieving a random decimal number from random.org."""
    result = get_random()

    # Assert that the result is the mocked random number
    assert result == RANDOM_NUMBER, f"Expected random number {RANDOM_NUMBER}, but got {result}"

    # Ensure that the correct URL was called
    requests.get.assert_called_once_with(
        "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new", timeout=5
    )

def test_get_random_request_failure(mocker):
    """Test handling of a request failure."""
    # Simulate a request failure by raising RequestException
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))

    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()

def test_get_random_timeout(mocker):
    """Test handling of a timeout."""
    # Simulate a timeout by raising Timeout
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()

def test_get_random_invalid_response(mock_random_org):
    """Test handling of an invalid response (non-float)."""
    # Simulate an invalid response that cannot be converted to a float
    mock_random_org.text = "invalid_response"

    with pytest.raises(ValueError, match="Invalid response from random.org: invalid_response"):
        get_random()