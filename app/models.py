from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Entry:
    pass


class ModelBase(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    status = Column(Integer, default=1)


class Game(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    teams = relationship('Team', backref="game", uselist=True)


class Team(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    game_id = Column(Integer, ForeignKey('game.id'))


class Event(ModelBase):
    title = Column(String(64), index=True, nullable=False)
    description = Column(String(120), index=True, nullable=True)
    game_id = Column(Integer, ForeignKey('game.id'))
    team1_id = Column(Integer, ForeignKey('team.id'))
    team2_id = Column(Integer, ForeignKey('team.id'))
