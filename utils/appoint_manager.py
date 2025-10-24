import json
import os.path
from typing import Final

from database.functions import get_all_managers

STATE_FILE: Final = "managers.json"


async def get_next_manager_id() -> int:
    managers = await get_all_managers()
    manager_ids = [manager[0] for manager in managers]

    last_id = None
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            last_id = data.get("last_appointed")

    if last_id in manager_ids:
        current_index = manager_ids.index(last_id)
        next_index = current_index + 1

        if next_index >= len(manager_ids):
            next_index = 0
    else:
        next_index = 0

    next_id = manager_ids[next_index]

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_appointed": next_id}, f)

    return next_id
