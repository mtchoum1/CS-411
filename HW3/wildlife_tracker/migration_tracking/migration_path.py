from typing import Optional

from wildlife_tracker.habitat_management.habitat import Habitat

class MigrationPath:

    def __init__(self, start_location: Habitat, status: str = "Scheduled") -> None:

        pass

    def update_migration_path_details(path_id: int, **kwargs) -> None:
        pass

    def get_migration_path_details(path_id) -> dict:
        pass