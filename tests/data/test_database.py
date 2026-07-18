import os

from dotenv import load_dotenv

from src.config import DB_HOST, DB_PORT, DB_NAME
from src.data.database import Database, PriceRepository
from src.data.sources.yfinance_source import YahooFinanceSource

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


def test_price_repository() -> None:

    # database and agent repository part
    database = Database(
        host=DB_HOST, 
        port=DB_PORT, 
        database_name=DB_NAME, 
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )
    repository = PriceRepository(database=database)

    # Source from Yahoo finance and dataframe from source
    source = YahooFinanceSource()
    price = source.get_price(["NVDA", "AMD"], "2026-01-01", "2026-01-10")

    with database.connect() as connexion:

        repository.save(
            price=price, 
            connexion=connexion
        )
        
        with connexion.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM prices
                WHERE ticker IN ('NVDA', 'AMD')
                AND date >= %s
                AND date < %s;""", 
                ("2026-01-01", "2026-01-10")
            )

            number_of_rows = cursor.fetchone()[0]
            assert number_of_rows == len(price)

        connexion.rollback()