from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Provider
from ..schemas import ProviderCreate, ProviderResponse

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get("", response_model=list[ProviderResponse])
def list_providers(db: Session = Depends(get_db)):
    return db.query(Provider).order_by(Provider.created_at.desc()).all()


@router.post("", response_model=ProviderResponse)
def create_provider(payload: ProviderCreate, db: Session = Depends(get_db)):
    row = db.query(Provider).filter(Provider.name == payload.name).first()
    if row:
        return row
    row = Provider(name=payload.name)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
