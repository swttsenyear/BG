from pydantic import BaseModel
from typing import List, Optional


class PositionCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None


class PositionUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class PositionResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class LessonCreate(BaseModel):
    position_id: int
    title: str
    description: Optional[str] = None
    step_order: int = 1


class LessonUpdate(BaseModel):
    position_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    step_order: Optional[int] = None
    is_active: Optional[bool] = None


class LessonResponse(BaseModel):
    id: int
    position_id: int
    title: str
    description: Optional[str] = None
    step_order: int
    is_active: bool

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    diamond_carat: Optional[float] = None
    diamond_count: Optional[int] = None
    material: Optional[str] = None
    gold_type: Optional[str] = None
    gold_weight: Optional[float] = None
    diamond_color: Optional[str] = None
    diamond_clarity: Optional[str] = None
    barcode: Optional[str] = None
    cost_code: Optional[str] = None
    selling_point: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    diamond_carat: Optional[float] = None
    diamond_count: Optional[int] = None
    material: Optional[str] = None
    gold_type: Optional[str] = None
    gold_weight: Optional[float] = None
    diamond_color: Optional[str] = None
    diamond_clarity: Optional[str] = None
    barcode: Optional[str] = None
    cost_code: Optional[str] = None
    selling_point: Optional[str] = None


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True


class DecodeRequest(BaseModel):
    code: str


class DecodeResponse(BaseModel):
    input_code: str
    decoded_number: str
    details: List[str]


class PriceRequest(BaseModel):
    cost_usd: float
    exchange_rate: float
    markup: float
    vat_percent: float = 0


class PriceResponse(BaseModel):
    cost_usd: float
    exchange_rate: float
    markup: float
    vat_percent: float
    cost_thb: float
    selling_price_before_vat: float
    vat_amount: float
    selling_price_final: float
    gross_profit: float
    margin_percent: float