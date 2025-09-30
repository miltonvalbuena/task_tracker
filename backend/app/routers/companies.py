from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Company, User
from app.schemas import Company as CompanySchema, CompanyCreate, CompanyUpdate, CompanyConfigUpdate
from app.auth import get_current_active_user, require_admin

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=CompanySchema)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/", response_model=List[CompanySchema])
def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

@router.get("/{company_id}", response_model=CompanySchema)
def read_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=CompanySchema)
def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = company_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    db.commit()
    db.refresh(company)
    return company

@router.put("/{company_id}/config", response_model=CompanySchema)
def update_company_config(
    company_id: int,
    config: CompanyConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Convertir la configuración a diccionario
    config_dict = [field.dict() for field in config.custom_fields_config]
    company.custom_fields_config = config_dict
    
    db.commit()
    db.refresh(company)
    return company

@router.get("/{company_id}/config")
def get_company_config(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return {"custom_fields_config": company.custom_fields_config}

@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(company)
    db.commit()
    return {"message": "Company deleted successfully"}
