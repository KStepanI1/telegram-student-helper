from sqlalchemy import Column, String, sql

from app.utils.db_api.db_gino import TimedBaseModel


class ZoomLink(TimedBaseModel):
    __tablename__ = 'links'
    subject_name = Column(String(100))
    lectures_code = Column(String(100))
    lectures_password = Column(String(100))
    lectures_link = Column(String(1000))
    practices_code = Column(String(100))
    practices_password = Column(String(100))
    practices_link = Column(String(1000))

    query: sql.Select
