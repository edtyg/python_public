import sqlalchemy
import pandas as pd

### Connection to DB ###
# google cloud pgsql db #
username = 'edgartan'
password = 'edgartan'
host = '34.87.63.225'
port = '5432'
database = 'trades'

db_url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(username, password, host, port, database)
engine = sqlalchemy.create_engine(db_url)
conn = engine.connect()


query = """

Select * from titanic_train
"""
result = conn.execute(query)
col_names = result.keys()
data = result.fetchall()

train = pd.DataFrame(data, columns = col_names)

###