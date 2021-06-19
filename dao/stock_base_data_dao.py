from customer_db import SqlAlchemy
from sqlalchemy.orm import sessionmaker
from model.stock_base_data import StockBaseData

engine = SqlAlchemy.get_engine()
Session = sessionmaker(bind=engine)


def get_stock_base_data_for_key(stock_date, stock_id):
    with Session() as session:
        return session.query(StockBaseData).filter(
            StockBaseData.stock_date == stock_date).filter(StockBaseData.stock_id == stock_id).order_by(
            StockBaseData.stock_id).all()


if __name__ == '__main__':
    stock_base_data_list = get_stock_base_data_for_key('20210617', "5269")
    print(type(stock_base_data_list))
    for stock_base_data in stock_base_data_list:
        print(stock_base_data)

