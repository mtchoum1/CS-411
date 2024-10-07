from typing import Optional

from wildlife_tracker.habitat_management.habitat import Habitat

class MigrationPath:

    def __init__(self, start_location: Habitat, start_date: str, current_date: str, destination: Habitat, duration: Optional[int] = None, status: str = "Scheduled") -> None:
        self.start_location = start_location
        self.status = status
        self.start_date = start_date
        self.current_date = current_date
        self.destination = destination
        self.duration = duration

    def update_migration_path_details(path_id: int, **kwargs) -> None:
        pass

    def get_migration_path_details(path_id) -> dict:
        pass