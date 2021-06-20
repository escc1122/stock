from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BIGINT, String, REAL
from customer_db import SqlAlchemy

Base = declarative_base()


# 建立一張資料表
class StockBaseData(Base):
    __tablename__ = 'stock_base_data'

    stock_date = Column(String(8), primary_key=True)
    stock_id = Column(String(10), primary_key=True)
    trade_volume = Column(BIGINT)
    closing_price = Column(REAL)
    opening_price = Column(REAL)
    lowest_price = Column(REAL)
    highest_price = Column(REAL)

    __table_args__ = (
        # UniqueConstraint('id', 'name', name='uix_id_name'),
        # Index('ix_id_name', 'name', 'extra'),
    )


# engine = create_engine(
#         "postgresql://scott:tiger@localhost/test:3306/dragon?charset=utf8",
#         max_overflow=0,  # 超過連線池大小外最多建立的連線
#         pool_size=5,  # 連線池大小
#         pool_timeout=30,  # 池中沒有執行緒最多等待的時間，否則報錯
#         pool_recycle=-1  # 多久之後對執行緒池中的執行緒進行一次連線的回收（重置）
#     )

if __name__ == '__main__':
    engine = SqlAlchemy.get_engine()
    Base.metadata.create_all(engine)
