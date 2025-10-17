from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import Task, User, Client
from app.schemas import Task as TaskSchema, TaskCreate, TaskUpdate
from app.auth import get_current_active_user

router = APIRouter(prefix="", tags=["tasks"])

@router.post("/tasks", response_model=TaskSchema)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Verificar que el cliente existe
    client = db.query(Client).filter(Client.id == task.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Verificar que el usuario asignado existe y pertenece al cliente
    if task.assigned_to:
        assigned_user = db.query(User).filter(User.id == task.assigned_to).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")
        if assigned_user.client_id != task.client_id:
            raise HTTPException(status_code=400, detail="Assigned user must belong to the same client")
    
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        client_id=task.client_id,
        assigned_to=task.assigned_to,
        created_by=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[TaskSchema])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    client_id: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Task)
    
    # Los usuarios solo pueden ver tareas de su cliente, excepto los admins
    if current_user.role != "admin":
        query = query.filter(Task.client_id == current_user.client_id)
    
    if client_id and client_id.strip():
        try:
            client_id_int = int(client_id)
            query = query.filter(Task.client_id == client_id_int)
        except ValueError:
            pass
    
    if assigned_to and assigned_to.strip():
        try:
            assigned_to_int = int(assigned_to)
            query = query.filter(Task.assigned_to == assigned_to_int)
        except ValueError:
            pass
    
    if status and status.strip():
        query = query.filter(Task.status == status)
    
    tasks = query.options(
        joinedload(Task.assigned_user),
        joinedload(Task.client),
        joinedload(Task.created_by_user)
    ).offset(skip).limit(limit).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskSchema)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = db.query(Task).options(
        joinedload(Task.assigned_user),
        joinedload(Task.client),
        joinedload(Task.created_by_user)
    ).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Los usuarios solo pueden ver tareas de su cliente, excepto los admins
    if current_user.role != "admin" and task.client_id != current_user.client_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return task

@router.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Los usuarios solo pueden actualizar tareas de su cliente, excepto los admins
    if current_user.role != "admin" and task.client_id != current_user.client_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = task_update.dict(exclude_unset=True)
    
    # Si se cambia el estado a completada, establecer completed_at
    if "status" in update_data and update_data["status"] == "completada":
        update_data["completed_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Los usuarios solo pueden eliminar tareas de su cliente, excepto los admins
    if current_user.role != "admin" and task.client_id != current_user.client_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
