from typing import Optional

from wildlife_tracker.habitat_management.habitat import Habitat

class MigrationPath:

    def __init__(self, path_id: int, current_date: str, current_location: str) -> None:
        self.current_location = current_location
        self.current_date = current_date
        self.path_id = path_id
    
    def create_migration_path(species: str, start_location: Habitat, destination: Habitat, duration: Optional[int] = None) -> None:
        pass

    def update_migration_path_details(self, **kwargs) -> None:
        pass

    def get_migration_path_details(self) -> dict:
        pass