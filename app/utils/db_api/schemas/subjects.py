from sqlalchemy import Column, String, sql, Integer

from app.utils.db_api.db_gino import TimedBaseModel


class Subject(TimedBaseModel):
    __tablename__ = "subjects"

    subject_id = Column(Integer(), primary_key=True)
    subject_name = Column(String(100))

    query: sql.Select
