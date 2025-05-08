import psycopg2
from psycopg2 import OperationalError
import yaml
with open('Util/paramsBD.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

def create_connection():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    connection = None
    try:
        connection = psycopg2.connect(
            database=config['Escola'],
            user=config['localhost'],
            password=config['faat'],
            host=config['faat'],
            port=config['2000'],
        )
        print("Conexão com o banco de dados PostgreSQL foi bem sucedida")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection
