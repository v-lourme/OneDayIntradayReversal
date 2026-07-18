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

    """Repository for storing and loading market prices."""

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

    def load(self, tickers: list[str], start_date: str, end_date: str, connexion: psycopg.Connection | None = None) -> pd.DataFrame:
        
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        if start_date >= end_date:
            raise ValueError("start_date must be earlier than end_date")
        
        if not tickers:
            raise ValueError("tickers must not be empty")
        
        tickers = list(dict.fromkeys(tickers))

        request = """
            SELECT 
                date, 
                ticker, 
                close, 
                high, 
                low, 
                open, 
                volume
            FROM prices
            WHERE ticker = ANY(%s)
            AND date >= %s
            AND date < %s
            ORDER BY date, ticker;
        """
        parameters = (tickers, start_date.date(), end_date.date())

        def execute_load(connexion: psycopg.Connection) -> pd.DataFrame:
            with connexion.cursor() as cursor:
                cursor.execute(request, parameters)
                rows = cursor.fetchall()

                return pd.DataFrame(
                    rows, 
                    columns=[
                        "Date", 
                        "Ticker", 
                        "Close", 
                        "High", 
                        "Low", 
                        "Open", 
                        "Volume"
                    ]
                )
        if connexion is None:
            with self.database.connect() as connexion:
                return execute_load(connexion)
            
        return execute_load(connexion)

    



