from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from config import host, USER, passwd, database, port
import datetime

# conn = "mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}?unix_socket=/var/run/mysqld/mysqld.sock".format(DB_USER, passwd,


conn = "mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(USER, passwd, host, port, database)
engine = create_engine(conn)
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    market_id = Column(Integer)
    price = Column(Integer)



    def __repr__(self):
        return "<Product ('%s', '%s')>" % (self.id, self.market_id)

# class Price(Base):
#     __tablename__ = 'prices'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     prId = Column(Integer, ForeignKey("products.id"))
#     price = Column(String(20), nullable=False)
#     date = Column(DateTime,default=datetime.date.today())
#     product = relationship("Product")
#
#     def __repr__(self):
#         return "<Price ('%s', '%s', '%s')>" % (self.prId, self.price, self.date)

class Root(Base):
    __tablename__='roots'
    id = Column(Integer, primary_key=True, autoincrement=True)
    root = Column(Integer)

    def __repr__(self):
        return "<Root ('%s')>" % (self.root)

Base.metadata.create_all(engine)