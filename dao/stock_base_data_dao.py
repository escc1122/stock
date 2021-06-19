from customer_db import SqlAlchemy
from sqlalchemy.orm import sessionmaker
from model.stock_base_data import StockBaseData

engine = SqlAlchemy.get_engine()
Session = sessionmaker(bind=engine)


def get_stock_base_data_for_key(stock_date, stock_id):
    with Session() as session:
        session.query(StockBaseData).filter(
            StockBaseData.stock_date == stock_date).filter(StockBaseData.stock_id == stock_id).order_by(
            StockBaseData.stock_id).all()


if __name__ == '__main__':
    get_stock_base_data_for_key('20210619', "2203")
