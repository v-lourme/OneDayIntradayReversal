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

    def save(self, price: pd.DataFrame) -> None:
        pass
    



