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


class Game(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    teams = relationship('Team', backref="game", uselist=True)
    events = relationship('Event', backref="game", uselist=True)
    schedules = relationship('Schedule', backref="game", uselist=True)


class Team(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    game_id = Column(Integer, ForeignKey(Game.id))


class Schedule(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    events = relationship('Event', backref="schedule", uselist=True)
    game_id = Column(Integer, ForeignKey(Game.id))


class Event(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    game_id = Column(Integer, ForeignKey(Game.id))
    schedule_id = Column(Integer, ForeignKey(Schedule.id))
    team1_id = Column(Integer, ForeignKey(Team.id))
    team2_id = Column(Integer, ForeignKey(Team.id))
    team1: ClassVar[Team] = relationship(Team, foreign_keys=[team1_id])
    team2: ClassVar[Team] = relationship(Team, foreign_keys=[team2_id])
