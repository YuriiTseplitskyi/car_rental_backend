from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine('mysql://root:Mcyura04@localhost:3306/car_rental')
metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()
