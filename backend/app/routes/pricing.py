from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ModelPricing
from ..schemas import PricingCreate, PricingResponse, PricingUpdate

router = APIRouter(prefix="/pricing", tags=["Pricing"])


@router.post("", response_model=PricingResponse)
def create_pricing(pricing: PricingCreate, db: Session = Depends(get_db)):
    row = ModelPricing(**pricing.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("", response_model=list[PricingResponse])
def list_pricing(db: Session = Depends(get_db)):
    return db.query(ModelPricing).order_by(ModelPricing.effective_from.desc()).all()


@router.put("/{pricing_id}", response_model=PricingResponse)
def update_pricing(
    pricing_id: int, pricing: PricingUpdate, db: Session = Depends(get_db)
):
    row = db.query(ModelPricing).filter(ModelPricing.id == pricing_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Pricing not found")
    for key, value in pricing.model_dump(exclude_unset=True).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{pricing_id}")
def delete_pricing(pricing_id: int, db: Session = Depends(get_db)):
    row = db.query(ModelPricing).filter(ModelPricing.id == pricing_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Pricing not found")
    db.delete(row)
    db.commit()
    return {"success": True}
