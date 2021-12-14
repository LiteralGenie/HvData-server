from . import Base

from sqlalchemy import Boolean, Column, Float, Integer, String

import enum, sqlalchemy


class LevelType(enum.Enum):
    NUMBER = enum.auto()
    SOULBOUND = enum.auto()
    UNASSIGNED = enum.auto()

class Equip(Base):
    __tablename__ = 'equip'

    id: int = Column(Integer, primary_key=True)
    key: str = Column(String, primary_key=True)

    last_updated: float = Column(Float, nullable=False)
    owner: str = Column(str)
    tradable: bool = Column(Boolean, nullable=False)
    type: str = Column(String, nullable=False)

    level: int = Column(Integer)
    level_type: LevelType = Column(sqlalchemy.Enum(LevelType), nullable=False)

    category: str = Column(String, nullable=False)
    condition_current: int = Column(Integer, nullable=False)
    condition_max: int = Column(Integer, nullable=False)
    potency_level: int = Column(Integer, nullable=False)
    potency_xp_current: int = Column(Integer)
    potency_xp_max: int = Column(Integer)
    
    damage: float = Column(Float)
    damage_type: str = Column(String)
    strike_1: str = Column(String)
    strike_2: str = Column(String)

    # main stats
    attack_accuracy: float = Column(Float)
    attack_crit_chance: float = Column(Float)
    attack_crit_damage: float = Column(Float)
    attack_speed: float = Column(Float)
    block_chance: float = Column(Float)
    burden: float = Column(Float)
    casting_speed: float = Column(Float)
    counter_parry: float = Column(Float)
    counter_resist: float = Column(Float)
    evade_chance: float = Column(Float)
    hp_bonus: float = Column(Float)
    interference: float = Column(Float)
    magic_accuracy: float = Column(Float)
    magic_damage: float = Column(Float)
    magical_mitigation: float = Column(Float)
    mana_conservation: float = Column(Float)
    parry_chance: float = Column(Float)
    physical_mitigation: float = Column(Float)
    resist_chance: float = Column(Float)
    spell_crit_damage: float = Column(Float)

    # mitigations
    cold: float = Column(Float)
    crushing: float = Column(Float)
    slashing: float = Column(Float)