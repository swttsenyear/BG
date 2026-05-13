from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import Base, engine, get_db
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Jewelry Training System API",
    description="Backend API สำหรับระบบเทรนพนักงานขายเพชร",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Jewelry Training System API is running",
        "docs": "/docs"
    }


# -------------------------
# Positions
# -------------------------

@app.post("/positions", response_model=schemas.PositionResponse)
def create_position(
    position: schemas.PositionCreate,
    db: Session = Depends(get_db)
):
    new_position = models.Position(
        code=position.code,
        name=position.name,
        description=position.description
    )

    try:
        db.add(new_position)
        db.commit()
        db.refresh(new_position)
        return new_position
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Position code already exists")


@app.get("/positions", response_model=list[schemas.PositionResponse])
def get_positions(db: Session = Depends(get_db)):
    return db.query(models.Position).order_by(models.Position.id).all()


@app.put("/positions/{position_id}", response_model=schemas.PositionResponse)
def update_position(
    position_id: int,
    position_update: schemas.PositionUpdate,
    db: Session = Depends(get_db)
):
    position = db.query(models.Position).filter(models.Position.id == position_id).first()

    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    update_data = position_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(position, key, value)

    try:
        db.commit()
        db.refresh(position)
        return position
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Position code already exists")


@app.delete("/positions/{position_id}")
def delete_position(
    position_id: int,
    db: Session = Depends(get_db)
):
    position = db.query(models.Position).filter(models.Position.id == position_id).first()

    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    db.query(models.Lesson).filter(models.Lesson.position_id == position_id).delete()
    db.delete(position)
    db.commit()

    return {"message": "Position deleted successfully"}


# -------------------------
# Lessons
# -------------------------

@app.post("/lessons", response_model=schemas.LessonResponse)
def create_lesson(
    lesson: schemas.LessonCreate,
    db: Session = Depends(get_db)
):
    position = db.query(models.Position).filter(models.Position.id == lesson.position_id).first()

    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    new_lesson = models.Lesson(
        position_id=lesson.position_id,
        title=lesson.title,
        description=lesson.description,
        step_order=lesson.step_order
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return new_lesson


@app.get("/lessons", response_model=list[schemas.LessonResponse])
def get_lessons(db: Session = Depends(get_db)):
    return db.query(models.Lesson).order_by(models.Lesson.step_order).all()


@app.get("/positions/{position_id}/lessons", response_model=list[schemas.LessonResponse])
def get_lessons_by_position(
    position_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Lesson)
        .filter(models.Lesson.position_id == position_id)
        .order_by(models.Lesson.step_order)
        .all()
    )


@app.put("/lessons/{lesson_id}", response_model=schemas.LessonResponse)
def update_lesson(
    lesson_id: int,
    lesson_update: schemas.LessonUpdate,
    db: Session = Depends(get_db)
):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    update_data = lesson_update.model_dump(exclude_unset=True)

    if "position_id" in update_data:
        position = db.query(models.Position).filter(
            models.Position.id == update_data["position_id"]
        ).first()

        if not position:
            raise HTTPException(status_code=404, detail="Position not found")

    for key, value in update_data.items():
        setattr(lesson, key, value)

    db.commit()
    db.refresh(lesson)

    return lesson


@app.delete("/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    db.delete(lesson)
    db.commit()

    return {"message": "Lesson deleted successfully"}


# -------------------------
# Products
# -------------------------

@app.post("/products", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = models.Product(**product.model_dump())

    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Product barcode already exists")


@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).order_by(models.Product.id).all()


@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Product barcode already exists")


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}


# -------------------------
# Barcode Decoder
# -------------------------

@app.post("/barcode/decode", response_model=schemas.DecodeResponse)
def decode_barcode(request: schemas.DecodeRequest):
    mapping = {
        "A": "1",
        "B": "2",
        "C": "3",
        "D": "4",
        "E": "5",
        "F": "6",
        "G": "7",
        "H": "8",
        "I": "9",
        "J": "0"
    }

    code = request.code.upper().strip()
    decoded_number = ""
    details = []

    for letter in code:
        if letter in mapping:
            decoded_number += mapping[letter]
            details.append(f"{letter} = {mapping[letter]}")
        else:
            details.append(f"{letter} = ไม่พบในระบบ")

    return {
        "input_code": code,
        "decoded_number": decoded_number,
        "details": details
    }


# -------------------------
# Price Calculator
# -------------------------

@app.post("/price/calculate", response_model=schemas.PriceResponse)
def calculate_price(request: schemas.PriceRequest):
    cost_thb = request.cost_usd * request.exchange_rate
    selling_price_before_vat = cost_thb * request.markup
    vat_amount = selling_price_before_vat * (request.vat_percent / 100)
    selling_price_final = selling_price_before_vat + vat_amount
    gross_profit = selling_price_final - cost_thb

    margin_percent = 0
    if selling_price_final > 0:
        margin_percent = (gross_profit / selling_price_final) * 100

    return {
        "cost_usd": request.cost_usd,
        "exchange_rate": request.exchange_rate,
        "markup": request.markup,
        "vat_percent": request.vat_percent,
        "cost_thb": cost_thb,
        "selling_price_before_vat": selling_price_before_vat,
        "vat_amount": vat_amount,
        "selling_price_final": selling_price_final,
        "gross_profit": gross_profit,
        "margin_percent": margin_percent
    }