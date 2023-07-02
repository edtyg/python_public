"""
sqlalchemy connector
creating tables child class
"""

from sqlalchemy_client import SqlAlchemyConnector

from local_credentials.db_credentials import AFTERSHOCK_PC_MAIN_ADMIN_LOCAL


class CreateTable(SqlAlchemyConnector):
    """inherits connector from parent class"""

    def create_table_sqlalchemy(self, table_name: str):
        """creates a table with your sqlalchemy connection"""

        # query = f"""
        # CREATE TABLE {table_name} (
        #     id BIGINT PRIMARY KEY,
        #     time TIMESTAMPTZ NOT NULL,
        #     market VARCHAR(50),
        #     baseCurrency VARCHAR(10),
        #     quoteCurrency VARCHAR(10),
        #     side VARCHAR(10),
        #     size FLOAT,
        #     fee FLOAT,
        #     feeCurrency VARCHAR(10)
        #     )
        # """
        query = "select * from ed_test"
        # try:
        self.connection.execute(query)
        # print("Table created")

        # except:
        #     print(error)


if __name__ == "__main__":
    client = CreateTable(AFTERSHOCK_PC_MAIN_ADMIN_LOCAL)
    client.postgres_connection()

    client.create_table_sqlalchemy("ed_test2")
