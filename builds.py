
import pandas as pd
import sqlalchemy
from sqlalchemy import text
from sqlalchemy.engine.mock import MockConnection


def save(connection: MockConnection, builds: pd.DataFrame, uid: str):
    with connection as con:
        con.execute(text(f"DELETE FROM builds WHERE player_uid = '{uid}'"))
        builds.to_sql(
            "builds",
            con=con,
            if_exists="append",
            index=False,
            dtype={
                "avatarInfo": sqlalchemy.types.JSON
            }
        )
        con.commit()
