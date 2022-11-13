from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from schema import Base


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    model = Column(String(45), nullable=False, unique=True)
    status = Column(Enum('new', 'old', 'used'), nullable=False)

    orders = relationship('Order', backref='cars')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=False)

    price = Column(Integer, nullable=False)
    status = Column(Enum('accepted', 'denied', 'unprocessed'), nullable=False)
    start_date = Column(DateTime, default=func.now(), nullable=False)
    end_date = Column(DateTime, default=func.now(), nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    password = Column(String(500), nullable=False)

    orders = relationship('Order', backref="users")
