from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey('type.id'), nullable=False)
    type = relationship(Type)


class Title(Base):
    __tablename__ = 'title'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    category = relationship(Category)


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    title_id = Column(Integer, ForeignKey('title.id'), nullable=False)
    title = relationship(Title)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    category = relationship(Category)


engine = create_engine('sqlite:///budget.db')
Base.metadata.create_all(engine)
