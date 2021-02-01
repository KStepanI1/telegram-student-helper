from sqlalchemy import Column, BigInteger, String, sql, Boolean

from app.utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    full_name = Column(String(100))
    subscription = Column(Boolean())
    admin = Column(Boolean())

    query: sql.Select
