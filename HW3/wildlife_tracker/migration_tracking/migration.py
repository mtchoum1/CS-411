from typing import Any

from wildlife_tracker.migration_tracking.migration_path import MigrationPath

class Migration:

    def __init__(self, migration_id: int, migration_path: MigrationPath, status: str = "Scheduled") -> None:
        pass

    def update_migration_details(migration_id: int, **kwargs: Any) -> None:
        pass

    def get_migration_details(migration_id: int) -> dict[str, Any]:
        pass

