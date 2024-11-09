import logging
from typing import List

from meal_max.models.kitchen_model import Meal, update_meal_stats
from meal_max.utils.logger import configure_logger
from meal_max.utils.random_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class BattleModel:
    """
    A class to manage battles of prepared meals

    Attributes:
        combatants(List[Meal]): The list of meals in battle
    """
    
    def __init__(self):
        """
        Initializes the BattleModel with an empty combatants list
        """
        self.combatants: List[Meal] = []

    def battle(self) -> str:
        """
        Completes the battle between combatants.

        Side-effects:
            Updates the combatants list to 1 by removing losing combatant
            Updates combatants stats

        Raises:
            ValueError: If a combatant list doesn't have 2 combatants
        """
        logger.info("Two meals enter, one meal leaves!")

        if self.get_combatants_length < 2:
            logger.error("Not enough combatants to start a battle.")
            raise ValueError("Two combatants must be prepped for a battle.")

        combatant_1 = self.combatants[0]
        combatant_2 = self.combatants[1]

        # Log the start of the battle
        logger.info("Battle started between %s and %s", combatant_1.meal, combatant_2.meal)

        # Get battle scores for both combatants
        score_1 = self.get_battle_score(combatant_1)
        score_2 = self.get_battle_score(combatant_2)

        # Log the scores for both combatants
        logger.info("Score for %s: %.3f", combatant_1.meal, score_1)
        logger.info("Score for %s: %.3f", combatant_2.meal, score_2)

        # Compute the delta and normalize between 0 and 1
        delta = abs(score_1 - score_2) / 100

        # Log the delta and normalized delta
        logger.info("Delta between scores: %.3f", delta)

        # Get random number from random.org
        random_number = get_random()

        # Log the random number
        logger.info("Random number from random.org: %.3f", random_number)

        # Determine the winner based on the normalized delta
        if delta > random_number:
            winner = combatant_1
            loser = combatant_2
        else:
            winner = combatant_2
            loser = combatant_1

        # Log the winner
        logger.info("The winner is: %s", winner.meal)

        # Update stats for both combatants
        update_meal_stats(winner.id, 'win')
        update_meal_stats(loser.id, 'loss')

        # Remove the losing combatant from combatants
        self.combatants.remove(loser)

        return winner.meal

    def clear_combatants(self):
        """
        Clears all combatants from the battle. If the battle is already empty, logs a warning.
        """

        logger.info("Clearing the combatants list.")
        if self.get_combatants_length == 0:
            logger.warning("Clearing an empty combatants list")
        self.combatants.clear()

    def get_battle_score(self, combatant: Meal) -> float:
        """
        Calculates combatants Score

        Args:
            combatant_data (Meal): the combatant to add to the combatant list.

        Raises:
            TypeError: If the combatant_data is not a valid Meal instance.
        """
        if not isinstance(combatant, Meal):
            logger.error("combatant_data is not a valid Meal")
            raise TypeError("combatant_data is not a valid Meal")
        
        difficulty_modifier = {"HIGH": 1, "MED": 2, "LOW": 3}

        # Log the calculation process
        logger.info("Calculating battle score for %s: price=%.3f, cuisine=%s, difficulty=%s",
                    combatant.meal, combatant.price, combatant.cuisine, combatant.difficulty)

        # Calculate score
        score = (combatant.price * len(combatant.cuisine)) - difficulty_modifier[combatant.difficulty]

        # Log the calculated score
        logger.info("Battle score for %s: %.3f", combatant.meal, score)

        return score

    def get_combatants(self) -> List[Meal]:
        """
        Returns a list of all combatant in the combatants list.
        """
        self.check_if_empty()
        logger.info("Retrieving current list of combatants.")
        return self.combatants

    def prep_combatant(self, combatant_data: Meal):
        """
        Adds a combatant to the combantant list.

        Args:
            combatant_data (Meal): the combatant to add to the combatant list.

        Raises:
            TypeError: If the combatant_data is not a valid Meal instance.
            ValueError: If a combatant list is full
        """
        if not isinstance(combatant_data, Meal):
            logger.error("combatant_data is not a valid Meal")
            raise TypeError("combatant_data is not a valid Meal")

        if len(self.combatants) >= 2:
            logger.error("Attempted to add combatant '%s' but combatants list is full", combatant_data.meal)
            raise ValueError("Combatant list is full, cannot add more combatants.")

        # Log the addition of the combatant
        logger.info("Adding combatant '%s' to combatants list", combatant_data.meal)

        self.combatants.append(combatant_data)

        # Log the current state of combatants
        logger.info("Current combatants list: %s", [combatant.meal for combatant in self.combatants])
    
    def check_if_empty(self) -> None:
        """
        Checks if the combatant is empty, logs an error, and raises a ValueError if it is.

        Raises:
            ValueError: If the combatant is empty.
        """
        if not self.combatants:
            logger.error("Combatant is empty")
            raise ValueError("Combatant is empty")
    
    def get_combatants_length(self) -> int:
        """
        Returns the number of combatant in the combatants list.
        """
        return len(self.combatants)
