from typing import ClassVar

from flask_sqlalchemy.model import _QueryProperty
from flask_sqlalchemy.query import Query
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Entry:
    pass


class ModelBase(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=func.now())
    status = Column(Integer, default=1)

    query: ClassVar[Query] = _QueryProperty()


class Schedule(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    teams = relationship('Team', backref="schedule", uselist=True)
    rounds = relationship('Round', backref="schedule", uselist=True)
    boards = relationship('Board', backref="schedule", uselist=True)


class Team(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    schedule_id = Column(Integer, ForeignKey(Schedule.id))


class Board(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    rounds = relationship('Round', backref="board", uselist=True)
    schedule_id = Column(Integer, ForeignKey(Schedule.id))


class Round(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    schedule_id = Column(Integer, ForeignKey(Schedule.id))
    board_id = Column(Integer, ForeignKey(Board.id))
    team1_id = Column(Integer, ForeignKey(Team.id))
    team2_id = Column(Integer, ForeignKey(Team.id))
    team1: ClassVar[Team] = relationship(Team, foreign_keys=[team1_id])
    team2: ClassVar[Team] = relationship(Team, foreign_keys=[team2_id])
