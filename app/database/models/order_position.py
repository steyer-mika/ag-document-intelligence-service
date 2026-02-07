from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base

class OrderPosition(Base):
    __tablename__ = "order_positions"

    id = Column(Integer, primary_key=True)
    extraction_result_id = Column(
        Integer,
        ForeignKey("extraction_results.id"),
        nullable=False,
    )

    # article_number
    article_number_value = Column(String, nullable=True)
    article_number_confidence = Column(Float, nullable=True)

    # description
    description_value = Column(String, nullable=True)
    description_confidence = Column(Float, nullable=True)

    # kvk
    kvk_value = Column(String, nullable=True)
    kvk_confidence = Column(Float, nullable=True)

    # wgp
    wgp_value = Column(String, nullable=True)
    wgp_confidence = Column(Float, nullable=True)

    # quantity
    quantity_value = Column(Float, nullable=True) # Do not use int, cause what if the unit is per karton/box instead of per piece? (:
    quantity_confidence = Column(Float, nullable=True)

    # price
    price_value = Column(Float, nullable=True)
    price_confidence = Column(Float, nullable=True)

    # total
    total_value = Column(Float, nullable=True)
    total_confidence = Column(Float, nullable=True)

    result = relationship("ExtractionResult", back_populates="positions")
