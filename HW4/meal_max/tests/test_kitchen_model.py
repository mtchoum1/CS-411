import pytest
from contextlib import contextmanager
import re
import sqlite3
from meal_max.models.kitchen_model import Meal, create_meal, delete_meal, get_leaderboard, get_meal_by_id, get_meal_by_name, update_meal_stats

######################################################
#
#    Fixtures and Utilities
#
######################################################

# Utility function to normalize SQL queries for testing
def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()

# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    # Mock the get_db_connection context manager
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn

    mocker.patch("meal_max.models.kitchen_model.get_db_connection", mock_get_db_connection)
    return mock_cursor

######################################################
#
#    Tests for create_meal
#
######################################################

def test_create_meal(mock_cursor):
    """Test creating a new meal entry."""
    create_meal("Pasta", "Italian", 12.99, "MED")
    expected_query = normalize_whitespace("""
        INSERT INTO meals (meal, cuisine, price, difficulty)
        VALUES (?, ?, ?, ?)
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query, "The SQL query did not match the expected structure."
    expected_args = ("Pasta", "Italian", 12.99, "MED")
    actual_args = mock_cursor.execute.call_args[0][1]
    assert actual_args == expected_args, f"Expected {expected_args}, got {actual_args}"

def test_create_meal_duplicate(mock_cursor):
    """Test error handling for duplicate meal entry."""
    mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
    with pytest.raises(ValueError, match="Meal with name 'Pasta' already exists"):
        create_meal("Pasta", "Italian", 12.99, "MED")

def test_create_meal_invalid_price():
    """Test error handling for invalid price."""
    with pytest.raises(ValueError, match="Price must be a positive number"):
        create_meal("Pasta", "Italian", -5, "MED")

def test_create_meal_invalid_difficulty():
    """Test error handling for invalid difficulty level."""
    with pytest.raises(ValueError, match="Invalid difficulty level"):
        create_meal("Pasta", "Italian", 12.99, "INVALID")

######################################################
#
#    Tests for delete_meal
#
######################################################

def test_delete_meal(mock_cursor):
    """Test soft deletion of a meal entry."""
    mock_cursor.fetchone.return_value = [False]
    delete_meal(1)
    expected_select_query = normalize_whitespace("SELECT deleted FROM meals WHERE id = ?")
    expected_update_query = normalize_whitespace("UPDATE meals SET deleted = TRUE WHERE id = ?")
    actual_select_query = normalize_whitespace(mock_cursor.execute.call_args_list[0][0][0])
    actual_update_query = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])
    assert actual_select_query == expected_select_query
    assert actual_update_query == expected_update_query

def test_delete_meal_not_found(mock_cursor):
    """Test handling for non-existent meal deletion."""
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        delete_meal(999)

def test_delete_meal_already_deleted(mock_cursor):
    """Test handling for deleting an already deleted meal."""
    mock_cursor.fetchone.return_value = [True]
    with pytest.raises(ValueError, match="Meal with ID 999 has been deleted"):
        delete_meal(999)

######################################################
#
#    Tests for get_leaderboard
#
######################################################

def test_get_leaderboard(mock_cursor):
    """Test leaderboard retrieval."""
    mock_cursor.fetchall.return_value = [
        (1, "Pasta", "Italian", 12.99, "MED", 5, 3, 60.0)
    ]
    leaderboard = get_leaderboard("win_pct")
    expected_result = [
        {'id': 1, 'meal': "Pasta", 'cuisine': "Italian", 'price': 12.99, 'difficulty': "MED", 'battles': 5, 'wins': 3, 'win_pct': 60.0}
    ]
    assert leaderboard == expected_result

def test_get_leaderboard_invalid_sort(mock_cursor):
    """Test error handling for invalid leaderboard sorting."""
    with pytest.raises(ValueError, match="Invalid sort_by parameter"):
        get_leaderboard("invalid_sort")

######################################################
#
#    Tests for get_meal_by_id
#
######################################################

def test_get_meal_by_id(mock_cursor):
    """Test retrieving a meal by ID."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 12.99, "MED", False)
    meal = get_meal_by_id(1)
    expected_meal = Meal(id=1, meal="Pasta", cuisine="Italian", price=12.99, difficulty="MED")
    assert meal == expected_meal

def test_get_meal_by_id_not_found(mock_cursor):
    """Test error handling for meal not found by ID."""
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Meal with ID 999 not found"):
        get_meal_by_id(999)

def test_get_meal_by_id_deleted(mock_cursor):
    """Test error handling for deleted meal retrieval by ID."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 12.99, "MED", True)
    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        get_meal_by_id(1)

######################################################
#
#    Tests for get_meal_by_name
#
######################################################

def test_get_meal_by_name(mock_cursor):
    """Test retrieving a meal by name."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 12.99, "MED", False)
    meal = get_meal_by_name("Pasta")
    expected_meal = Meal(id=1, meal="Pasta", cuisine="Italian", price=12.99, difficulty="MED")
    assert meal == expected_meal

def test_get_meal_by_name_not_found(mock_cursor):
    """Test error handling for meal not found by name."""
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Meal with name Pasta not found"):
        get_meal_by_name("Pasta")

def test_get_meal_by_name_deleted(mock_cursor):
    """Test error handling for deleted meal retrieval by name."""
    mock_cursor.fetchone.return_value = (1, "Pasta", "Italian", 12.99, "MED", True)
    with pytest.raises(ValueError, match="Meal with name Pasta has been deleted"):
        get_meal_by_name("Pasta")

######################################################
#
#    Tests for update_meal_stats
#
######################################################

def test_update_meal_stats_win(mock_cursor):
    """Test updating meal stats with a win."""
    mock_cursor.fetchone.return_value = [False]
    update_meal_stats(1, "win")
    expected_update_query = normalize_whitespace("UPDATE meals SET battles = battles + 1, wins = wins + 1 WHERE id = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])
    assert actual_query == expected_update_query

def test_update_meal_stats_loss(mock_cursor):
    """Test updating meal stats with a loss."""
    mock_cursor.fetchone.return_value = [False]
    update_meal_stats(1, "loss")
    expected_update_query = normalize_whitespace("UPDATE meals SET battles = battles + 1 WHERE id = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])
    assert actual_query == expected_update_query

def test_update_meal_stats_invalid_result(mock_cursor):
    """Test error handling for invalid result type in meal stats update."""
    mock_cursor.fetchone.return_value = [False]  # Simulate that the meal exists and is not deleted.
    with pytest.raises(ValueError, match="Invalid result: invalid. Expected 'win' or 'loss'."):
        update_meal_stats(1, "invalid")

def test_update_meal_stats_deleted_meal(mock_cursor):
    """Test error handling for updating stats of a deleted meal."""
    mock_cursor.fetchone.return_value = [True]
    with pytest.raises(ValueError, match="Meal with ID 1 has been deleted"):
        update_meal_stats(1, "win")