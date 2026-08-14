from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ApiUsage
from ..schemas import UsageDataIn, UsageResponse
from ..services.usage_service import create_usage

router = APIRouter(prefix="/usage", tags=["Usage"])


@router.post("", response_model=UsageResponse)
def post_usage(payload: UsageDataIn, db: Session = Depends(get_db)):
    return create_usage(db, payload.model_dump())


@router.get("", response_model=list[UsageResponse])
def list_usage(db: Session = Depends(get_db)):
    return db.query(ApiUsage).order_by(ApiUsage.timestamp.desc()).limit(1000).all()


@router.get("/{usage_id}", response_model=UsageResponse)
def get_usage(usage_id: int, db: Session = Depends(get_db)):
    row = db.query(ApiUsage).filter(ApiUsage.id == usage_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Usage not found")
    return row
