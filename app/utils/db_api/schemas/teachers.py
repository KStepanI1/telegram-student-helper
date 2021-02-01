from sqlalchemy import Column, String, sql, Integer

from app.utils.db_api.db_gino import TimedBaseModel
from app.utils.db_api.schemas.subjects import Subject


class Teachers(TimedBaseModel):
    __tablename__ = "teachers"

    teacher_id = Column(Integer(), primary_key=True)
    subject_name = Subject.subject_name
    teacher_name = Column(String(100))
    kind_of_activity = Column(String(100))
    teacher_mail = Column(String(100))

    query: sql.Select
