import os
import sys
import logging
from sqlalchemy import create_engine, Table, Column, String, MetaData, Date
from sqlalchemy.schema import CreateSchema

class Db:
    '''
    This class represents a the connection to the database holding the 'users' table

    Attributes
    ----------
    host : str
        database hostname. Default is taken from environment variable DB_HOST
    port : str
        database port. Default is taken from environment variable DB_PORT
    user : str
        username to connect to database. Default is taken from environment variable DB_USER
    password : str
        password to connect to database. Default is taken from environment variable DB_PASSWORD
    name : str
        database name. Default is 'revolut'
    schema : str
        database schema. Default is 'revolut'    
    '''
    def __init__(self, username:str, password:str, host:str='localhost', port:str='5432', name:str='revolut', schema:str='revolut'):
        self.db = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{name}')

        self.users = Table('users', MetaData(self.db), 
                            Column('username', String, primary_key=True),
                            Column('dateofbirth', Date),
                            schema=schema)
        
        if 'LOG_LEVEL' in os.environ:
            log_level = os.environ['LOG_LEVEL']
        else:
             log_level = 'INFO'
        logging.basicConfig(level=log_level,stream=sys.stdout,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log = logging.getLogger(type(self).__name__)


    def write_user(self, username:String, dateOfBirth:Date) -> None:
        '''
        This method writes a user to the Db

        Parameters
        ----------
        username : str
            A username
        dateOfBirth: Date
            The user's date of birth 

        Raises
        ------
        Exception
            if the record cannot be inserted
        '''
        with self.db.connect() as conn:
            statement = self.users.insert().values(username=username, dateofbirth=dateOfBirth)
            try:    
                conn.execute(statement)
                self.log.info(f'username {username} with birthday {dateOfBirth} was inserted')
                return
            except Exception as e:
                self.log.error(f'Cannot insert {username} with birthday {dateOfBirth} - {e}')
                raise e


    def read_user(self, username:str) -> (str, Date):
        '''
        read user from Db

        Parameters
        ----------
        username : str
            A username

        Returns
        ----------
        username : str
            the users username
        birthday : Date
            the users birthday

        Raises
        ------
        Exception
            If the record was not found
        '''
        with self.db.connect() as conn:
            statement = self.users.select().where(self.users.c.username == username)
            try:
                result = conn.execute(statement)
                if result.rowcount == 1: 
                    user = result.first()
                    self.log.info(f'username {user[0]} with birthday {user[1]} was retrieved') 
                    return user[0],user[1]
                else:
                    raise Exception('User not found')
            except Exception as e:
                self.log.error(f'Cannot get user {username} - {e}')    
                raise e

    def read_databases(self):
        with self.db.connect() as conn:
            conn.execute("SELECT datname FROM pg_database")