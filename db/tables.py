import json

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine.mock import MockConnection


def get_saved_builds(connection: MockConnection, uid: str) -> list:
    with connection as con:
        query = text(f"SELECT * FROM builds WHERE player_uid = '{uid}'")
        saved_showcase = pd.read_sql(query, con=con)

        saved_showcase["avatarInfo"] = (
            saved_showcase["avatarInfo"].apply(json.loads)
        )
        saved_showcase["index"] = saved_showcase["character_name"]
        saved_showcase.set_index("index", inplace=True)

    return saved_showcase.copy()
