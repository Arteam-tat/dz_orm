import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from mod import create_tables, Publisher, Shop, Book, Stock, Sale

load_dotenv()
DSN = os.getenv("DSN")
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

with open('dz/ORM/py-homeworks-db/orm/fixtures/tests_data.json', 'r') as fd:
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
while True:
    publ = input('Введите фамилию автора:')
    if publ in session.query(Publisher.name):
        for d in session.query(Publisher.name).join(Book.name).join(Shop.name).join(Sale.price).\
                join(Sale.date_sale).filter.like(publ).all():
            print(d)
    else:
        print(f'Автора - {publ}, нет в списке')
session.commit()



session.close()