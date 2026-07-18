import psycopg


class Database:
    
    def __init__(self, host: str, port: int, database_name: str, user: str, password: str) -> None:
        self.host = str(host)
        self.port = int(port)
        self.database_name = str(database_name)
        self.user = str(user)
        self.password = str(password)

    def connect(self) -> psycopg.Connection:
        pass

    def test(self) -> None:
        pass



