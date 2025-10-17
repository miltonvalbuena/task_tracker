from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Client, User
from app.schemas import Client as ClientSchema, ClientCreate, ClientUpdate, ClientConfigUpdate
from app.auth import get_current_active_user, require_admin

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientSchema)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/", response_model=List[ClientSchema])
def read_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients

@router.get("/{client_id}", response_model=ClientSchema)
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientSchema)
def update_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    update_data = client_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)
    
    db.commit()
    db.refresh(client)
    return client

@router.put("/{client_id}/config", response_model=ClientSchema)
def update_client_config(
    client_id: int,
    config: ClientConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Convertir la configuración a diccionario
    config_dict = [field.dict() for field in config.custom_fields_config]
    client.custom_fields_config = config_dict
    
    db.commit()
    db.refresh(client)
    return client

@router.get("/{client_id}/config")
def get_client_config(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return {"custom_fields_config": client.custom_fields_config}

@router.delete("/{client_id}")
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}
