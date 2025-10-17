from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ARL, User
from app.schemas import ARLCreate, ARLUpdate, ARL as ARLSchema
from app.auth import require_admin

router = APIRouter(prefix="/arls", tags=["arls"])

@router.post("/", response_model=ARLSchema)
def create_arl(
    arl: ARLCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Crear una nueva ARL"""
    db_arl = ARL(**arl.dict())
    db.add(db_arl)
    db.commit()
    db.refresh(db_arl)
    return db_arl

@router.get("/", response_model=list[ARLSchema])
def read_arls(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Obtener lista de ARLs"""
    arls = db.query(ARL).filter(ARL.is_active == True).offset(skip).limit(limit).all()
    return arls

@router.get("/{arl_id}", response_model=ARLSchema)
def read_arl(
    arl_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Obtener una ARL específica"""
    arl = db.query(ARL).filter(ARL.id == arl_id).first()
    if not arl:
        raise HTTPException(status_code=404, detail="ARL not found")
    return arl

@router.put("/{arl_id}", response_model=ARLSchema)
def update_arl(
    arl_id: int,
    arl_update: ARLUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Actualizar una ARL"""
    arl = db.query(ARL).filter(ARL.id == arl_id).first()
    if not arl:
        raise HTTPException(status_code=404, detail="ARL not found")
    
    update_data = arl_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(arl, field, value)
    
    db.commit()
    db.refresh(arl)
    return arl

@router.delete("/{arl_id}")
def delete_arl(
    arl_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Eliminar una ARL (soft delete)"""
    arl = db.query(ARL).filter(ARL.id == arl_id).first()
    if not arl:
        raise HTTPException(status_code=404, detail="ARL not found")
    
    arl.is_active = False
    db.commit()
    return {"message": "ARL deleted successfully"}
