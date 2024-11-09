import pytest

from meal_max.models.kitchen_model import Meal
from meal_max.models.battle_model import BattleModel

@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

"""Fixtures providing sample combatants for the tests."""
@pytest.fixture
def sample_meal1():
    return Meal(1,"Dumplings","Chinese",100,"LOW")

@pytest.fixture
def sample_meal2():
    return Meal(2,"Steak","American",50,"MED")

@pytest.fixture
def sample_meal3():
    return Meal(3,"Spagetti","Italian",150,"HIGH")

@pytest.fixture
def sample_combatantslist(sample_meal1, sample_meal2):
    return [sample_meal1, sample_meal2]

def test_prep_combatant(battle_model, sample_meal1):
    """Test adding a meal to the combatant."""
    battle_model.prep_combatant(sample_meal1)
    assert battle_model.get_combatants_length == 1
    assert battle_model.get_combatants[0].meal == 'Dumplings'

def test_adding_non_meal_to_combatant(battle_model, non_meal):
    """Test error when adding a non Meal type to the combatant."""
    with pytest.raises(ValueError, match="combatant_data is not a valid Meal"):
        battle_model.prep_combatant(non_meal)

def test_adding_third_meal_to_combatant(battle_model, sample_meal1, sample_meal2, sample_meal3):
    """Test error when adding a third meal to the combatant."""
    battle_model.prep_combatant(sample_meal1)
    assert battle_model.get_combatants_length == 1
    assert battle_model.get_combatants[0].meal == 'Dumplings'
    battle_model.prep_combatant(sample_meal2)
    assert battle_model.get_combatants_length == 2
    assert battle_model.get_combatants[1].meal == 'Steak'
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal3)

def test_clear_combatants(battle_model, sample_meal1):
    """Test clearing the entire combatant list."""
    battle_model.prep_combatant(sample_meal1)

    battle_model.clear_combatants()
    assert battle_model.get_combatants_length == 0, "combatants list should be empty after clearing"

def test_clear_combatants_empty_combatants(playlist_model, caplog):
    """Test clearing the entire combatants list when it's empty."""
    battle_model.clear_combatants()
    assert battle_model.get_combatants_length == 0, "combatants list should be empty after clearing"
    assert "Clearing an empty combatants list " in caplog.text, "Expected warning message when clearing an empty combatants list"

def test_get_battle_score(battle_model, non_meal):
    """Test error when adding a non Meal type to the combatant."""
    with pytest.raises(ValueError, match="combatant_data is not a valid Meal"):
        battle_model.get_battle_score(non_meal)

def test_check_if_empty_non_empty_playlist(playlist_model, sample_song1):
    """Test check_if_empty does not raise error if combatants is not empty."""
    battle_model.prep_combatant(sample_meal1)
    try:
        battle_model.check_if_empty()
    except ValueError:
        pytest.fail("check_if_empty raised ValueError unexpectedly on non-empty playlist")

def test_check_if_empty_empty_playlist(playlist_model):
    """Test check_if_empty raises error when combatants is empty."""
    battle_model.clear_combatants()
    with pytest.raises(ValueError, match="Combatant is empty"):
        battle_model.check_if_empty()

def test_battle_with_one_meal_battles(battle_model, sample_meal1):
    battle_model.prep_combatant(sample_meal1)
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.check_if_empty()

