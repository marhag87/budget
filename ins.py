from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from alch import Base, Transaction, Title, Category, Type
from datetime import datetime

engine = create_engine('sqlite:///budget.db')
Base.metadata.bind = engine
session = sessionmaker(bind=engine)()

try:
    home = Type(name='Home')
    session.add(home)
    session.commit()
except IntegrityError:
    session.rollback()
    home = session.query(Type).filter(Type.name == 'Home').one()

try:
    rent = Category(name='Rent', type=home)
    session.add(rent)
    session.commit()
except IntegrityError:
    session.rollback()
    rent = session.query(Category).filter(Category.name == 'Rent').one()

try:
    stangastaden = Title(name='Stångåstaden', category=rent)
    session.add(stangastaden)
    session.commit()
except IntegrityError:
    session.rollback()
    stangastaden = session.query(Title).filter(Title.name == 'Stångåstaden').one()


try:
    rent_february = Transaction(
        amount=-6576,
        balance=20079.12,
        date=datetime.strptime('2018-02-28', '%Y-%m-%d').date(),
        title=stangastaden,
    )
    session.add(rent_february)
    session.commit()
except IntegrityError:
    session.rollback()
    rent_february = session.query(Transaction).filter(Transaction.title == stangastaden).one()


print(rent_february.amount)
print(rent_february.date)
