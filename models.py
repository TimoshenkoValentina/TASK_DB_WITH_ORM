import sqlalchemy as sql
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Shop(Base):
    __tablename__ = 'shop'

    shop_id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(length=100), unique=True, nullable=False)

    def __str__(self):
        return self.name


class Publisher(Base):
    __tablename__ = 'publisher'

    publisher_id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(length=100), unique=True, nullable=False)

    def __str__(self):
        return f'id={self.id}, автор - {self.name}'


class Book(Base):
    __tablename__ = 'book'

    book_id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String(length=100), unique=True, nullable=False)
    id_publisher = sql.Column(sql.Integer, sql.ForeignKey('publisher.publisher_id'), nullable=False)

    publisher = relationship(Publisher, backref='book')


class Stock(Base):
    __tablename__ = 'stock'

    stock_id = sql.Column(sql.Integer, primary_key=True)
    book_id = sql.Column(sql.Integer, sql.ForeignKey('book.book_id'), nullable=False)
    shop_id = sql.Column(sql.Integer, sql.ForeignKey('shop.shop_id'), nullable=False)
    count = sql.Column(sql.Integer, nullable=False)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='Stock')


class Sale(Base):
    __tablename__ = 'sale'

    sale_id = sql.Column(sql.Integer, primary_key=True)
    price = sql.Column(sql.Float, nullable=False)
    date_sale = sql.Column(sql.DateTime, nullable=False)
    id_stock = sql.Column(sql.Integer, sql.ForeignKey('stock.stock_id'), nullable=False)
    count = sql.Column(sql.Integer, nullable=False)

    stock = relationship(Stock, backref='sale')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
