from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from alch import Base, Category, Type

engine = create_engine('sqlite:///budget.db')
Base.metadata.bind = engine
session = sessionmaker(bind=engine)()


def budget_type(*, name=None):
    try:
        result = Type(name=name)
        session.add(result)
        session.commit()
    except IntegrityError:
        session.rollback()
        result = session.query(Type).filter(Type.name == name).one()
    return result


def budget_category(*, name=None, parent=None):
    try:
        result = Category(name=name, type=parent)
        session.add(result)
        session.commit()
    except IntegrityError:
        session.rollback()
        result = session.query(Category).filter(Category.name == name).one()
    return result


home = budget_type(name='Home')
budget_category(name='Rent', parent=home)
budget_category(name='Insurance', parent=home)
budget_category(name='Electricity', parent=home)
budget_category(name='Loan repayment', parent=home)
budget_category(name='Phone', parent=home)
budget_category(name='Internet', parent=home)
budget_category(name='Furnishing', parent=home)
budget_category(name='Appliances', parent=home)
budget_category(name='Garden', parent=home)
budget_category(name='Other', parent=home)

transportation = budget_type(name='Transportation')
budget_category(name='Car lease', parent=transportation)
budget_category(name='Fuel', parent=transportation)
budget_category(name='Parking', parent=transportation)
budget_category(name='Insurance', parent=transportation)
budget_category(name='Public transportation', parent=transportation)

daily_living = budget_type(name='Daily living')
budget_category(name='Groceries', parent=daily_living)
budget_category(name='Dining out', parent=daily_living)
budget_category(name='Going out', parent=daily_living)
budget_category(name='Clothing', parent=daily_living)
budget_category(name='Haircut', parent=daily_living)
budget_category(name='Alcohol', parent=daily_living)

entertainment = budget_type(name='Entertainment')
budget_category(name='Games', parent=entertainment)
budget_category(name='Electronics', parent=entertainment)
budget_category(name='Shooting', parent=entertainment)
budget_category(name='Entertainment', parent=entertainment)
budget_category(name='Subscriptions', parent=entertainment)

health = budget_type(name='Health')
budget_category(name='Medicine', parent=health)
budget_category(name='Insurance', parent=health)

income = budget_type(name='Income')
budget_category(name='Salary', parent=income)
budget_category(name='Refunds / Reimbursements', parent=income)
