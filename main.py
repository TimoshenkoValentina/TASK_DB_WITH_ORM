import sqlalchemy
from sqlalchemy.orm import sessionmaker

from ORM.funcs import fill_schema, find_info
from models import create_tables


if __name__ == "__main__":

    DB_USER = input('Необходимо ввести логин: ')
    DB_PASSWORD = input('Необходимо ввести пароль: ')

    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'postgres'

    DSN = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    fill_schema(session)
    find_info(session)

    session.close()


