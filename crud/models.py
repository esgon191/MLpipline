import datetime
from typing import Optional, Annotated
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc+3', now())"))]

class Photo(Base):
    __tablename__ = "photo"

    id: Mapped[intpk]
    latitude: Mapped[float]    
    longitude: Mapped[float]
    created_at: Mapped[created_at]
    is_processed: Mapped[bool]

class RoadSign(Base):
    """known roadsignes (predifined)"""
    
    __tablename__ = "roadsign"
    id: Mapped[intpk] 
    number: Mapped[str]
    name: Mapped[str]
    

class BoundBoxAble(Base):
    """Абстрактный для найденных знаков и дефектов"""

    id: Mapped[intpk]
    confidence: Mapped[float]
    created_at: Mapped[created_at]
    x1: Mapped[float]
    x2: Mapped[float]
    y1: Mapped[float]
    y2: Mapped[float]


class DetectedSign(BoundBoxAble):
    __tablename__ = "detected_sign"
    
    photo_id: Mapped[int] = mapped_column(ForeignKey("photo.id", ondelete="CASCADE"))
    roadsign_type: Mapped[int] = mapped_column(ForeignKey("roadsign.id"))


class Defect(Base):
    __tablename__ = "defect"

    id: Mapped[intpk]
    name: Mapped[str]
    

class DetectedDefect(BoundBoxAble):
    __tablename__ = "detected_defect"
    
    detected_sign_id: Mapped[int] = mapped_column(ForeignKey("photo.id"))
    defect_type_id: Mapped[int] = mapped_column(ForeignKey("defect.id"))
