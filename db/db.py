
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine


def showcase_db_connection():
    user = os.environ.get("DB_USER")
    password = quote_plus(os.environ.get("DB_PASSWORD"))
    host = os.environ.get("DB_HOST")
    database = os.environ.get("DB_NAME")

    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}"
    )
    connection = engine.connect()
    return connection
