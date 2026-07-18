import psycopg
import pandas as pd


class Database:

    """ Database initiates a connexion to TimeScaleDB """
    
    def __init__(self, host: str, port: int, database_name: str, user: str, password: str) -> None:
        self.host = str(host)
        self.port = int(port)
        self.database_name = str(database_name)
        self.user = str(user)
        self.password = str(password)

    def connect(self) -> psycopg.Connection:
        return psycopg.connect(host = self.host, 
                               port = self.port, 
                               dbname = self.database_name, 
                               user = self.user, 
                               password = self.password)
    

class PriceRepository:

    """ Save, Load, Update and Delete prices from the database"""

    def __init__(self, database: Database) -> None:
        self.database = database

    def save(self, price: pd.DataFrame, connexion: psycopg.Connection | None = None) -> None:
        
        upsert_query = """
                INSERT INTO prices (
                    date, 
                    ticker, 
                    close, 
                    high, 
                    low, 
                    open, 
                    volume
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (date, ticker)
                DO UPDATE SET
                    close = EXCLUDED.close, 
                    high = EXCLUDED.high, 
                    low = EXCLUDED.low, 
                    open = EXCLUDED.open, 
                    volume = EXCLUDED.volume
        """

        rows = list(
            price[
                ["Date", "Ticker", "Close", "High", "Low", "Open", "Volume"]
            ].itertuples(index=False, name=None)
        )

        if connexion is None:
            with self.database.connect() as connexion:
                with connexion.cursor() as cursor:
                    cursor.executemany(upsert_query, rows)

        else:
            with connexion.cursor() as cursor:
                cursor.executemany(upsert_query, rows)
    



