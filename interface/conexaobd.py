import psycopg2
from config import config

class Banco():
    def __init__(self):
        """ Connect to the PostgreSQL database server """
        self.conexao = None
        try:
            # read connection parameters
            params = config()
            # connect to the PostgreSQL server
            print('Conectando ao banco de dados PostgreSQL ...')
            self.conexao = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conexao is not None:
                print('Conexão bem sucessidade!')

        
