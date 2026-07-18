import os

from dotenv import load_dotenv

from src.config import DB_HOST, DB_PORT, DB_NAME
from src.data.database import Database

load_dotenv()

def test_database_connexion() -> None:
    database = Database(
        host=DB_HOST, 
        port=DB_PORT, 
        database_name=DB_NAME, 
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

    with database.connect() as connexion:
        with connexion.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

    assert result == (1,)