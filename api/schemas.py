from datetime import datetime

from sqlalchemy import Boolean, Column, String, Integer, DateTime, text, TIMESTAMP, func

from api.database import Base


# class User(Base):
#     __tablename__ = "userslist"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     surname = Column(String)
#     is_active = Column(Boolean, default=True)


class IdGeneratorSql(Base):
    __tablename__ = "room_ids"

    sr_no = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(String, unique=True)
    name = Column(String, index=True)
    mobile_number = Column(String, index=True)
    is_active = Column(Boolean, default=True)


class PeopleWithId(Base):
    __tablename__ = "peoplewitgid"

    sr_no = Column(Integer, primary_key=True, autoincrement=True)
    room_id_new = Column(String, index=True)
    name = Column(String, index=True)
    mobile_number = Column(String, index=True)


class CreatePostWithId(Base):
    __tablename__ = "userpost"

    sr_no = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(String, index=True)
    mobile_number = Column(String, index=True)
    created_by_name = Column(String, index=True)
    title = Column(String, index=True)
    task_assign_to = Column(String, index=True)
    time_to_finish = Column(String, index=True)
    date_time = Column(String, index=True)
    before_after = Column(String, index=True)
    possible_if = Column(String, index=True)
    task_des = Column(String, index=True)
    post_id = Column(Integer, autoincrement=True, index=True, unique=True)
    is_active = Column(String, index=True)
    img_url = Column(String, index=True)
    created_at = Column(DateTime, index=True, default=datetime.now)
    updated_at = Column(DateTime, index=True, default=datetime.now(), onupdate=date_time.onupdate)
