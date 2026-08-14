from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Model
from ..schemas import ModelCreate, ModelResponse

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("", response_model=list[ModelResponse])
def list_models(db: Session = Depends(get_db)):
    return db.query(Model).order_by(Model.created_at.desc()).all()


@router.post("", response_model=ModelResponse)
def create_model(payload: ModelCreate, db: Session = Depends(get_db)):
    row = (
        db.query(Model)
        .filter(
            Model.provider_id == payload.provider_id,
            Model.model_name == payload.model_name,
        )
        .first()
    )
    if row:
        return row
    row = Model(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
