from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)

    lessons = relationship("Lesson", back_populates="position")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    position_id = Column(Integer, ForeignKey("positions.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    step_order = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    position = relationship("Position", back_populates="lessons")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    diamond_carat = Column(Float)
    diamond_count = Column(Integer)
    material = Column(String)
    gold_type = Column(String)
    gold_weight = Column(Float)
    diamond_color = Column(String)
    diamond_clarity = Column(String)
    barcode = Column(String, unique=True)
    cost_code = Column(String)
    selling_point = Column(String)


class CodeMapping(Base):
    __tablename__ = "code_mappings"

    id = Column(Integer, primary_key=True, index=True)
    letter = Column(String, unique=True, nullable=False)
    number = Column(String, nullable=False)


class PriceFormula(Base):
    __tablename__ = "price_formulas"

    id = Column(Integer, primary_key=True, index=True)
    exchange_rate = Column(Float, default=36)
    markup = Column(Float, default=2.5)
    vat_percent = Column(Float, default=7)