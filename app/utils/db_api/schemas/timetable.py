from sqlalchemy import String, Column, sql

from app.utils.db_api.db_gino import TimedBaseModel


class Couples(TimedBaseModel):
    __tablename__ = "couples"

    couple_ui = Column(String(100))
    time_start = Column(String(20))
    time_end = Column(String(20))
    name_couple_odd = Column(String(100))
    name_couple_even = Column(String(100))
    time_break = Column(String(20))

    query: sql.Select



