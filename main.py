import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale


def fill_schema(session):

    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def find_info(session):
    publish = input('Для начала поиска введите имя автора или его id: ')
    if publish.isdigit():
        for pub in session.query(Publisher).filter(Publisher.id == int(publish)).all():
            print(pub)
        print('Информация о продажах книг - точки продаж, стоимость товара, время покупки : ')
        for s in session.query(Shop).join(Stock.shop).join(Book).join(Publisher).filter(Publisher.id==int(publish)).all():
            print(s)
    else:
        for pub in session.query(Publisher).filter(Publisher.name.like(publish)).all():
            print(pub)
        print('Информация о продажах книг - точки продаж, стоимость товара, время покупки : ')
        for s in session.query(Shop).join(Stock.shop).join(Book).join(Publisher).filter(Publisher.name==publish).all():
            print(s)


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


