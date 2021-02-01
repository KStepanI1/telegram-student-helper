from sqlalchemy import Column, String, sql, Integer

from app.utils.db_api.db_gino import TimedBaseModel


class Events(TimedBaseModel):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    subject_name = Column(String(100))
    name = Column(String(100))
    date = Column(String(100))
    time = Column(String(100))

    query: sql.Select
