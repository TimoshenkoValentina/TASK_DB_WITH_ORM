import json
from models import Publisher, Shop, Book, Stock, Sale


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
    publisher_info = input('\nДля начала поиска введите имя автора или его id: ')

    sale_data = session.query(
            Book.title, Shop.name, Sale.price, Sale.date_sale
        ).select_from(Shop).\
        join(Stock.shop).\
        join(Sale).\
        join(Book).\
        join(Publisher)

    if publisher_info.isdigit():
        for publisher in session.query(Publisher).filter(Publisher.id == int(publisher_info)).all():
            print('\n' f"Введенный id: {publisher.id}, соответствует автору: {publisher.name}")
        publisher_data = sale_data.filter(Publisher.id == int(publisher_info)).all()
    else:
        for publisher in session.query(Publisher).filter(Publisher.name.like(publisher_info)).all():
            print('\n' f"Введенный автор: {publisher.name}, соответствующий ему id: {publisher.id}")
        publisher_data = sale_data.filter(Publisher.name.like(publisher_info)).all()
    print('\nИнформация о продажах книг - точки продаж, стоимость товара, время покупки: ')
    for title, name, price, date_sale in publisher_data:
        print(f"{title: <40} | {name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")
