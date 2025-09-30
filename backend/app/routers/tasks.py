from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import Task, User, Company
from app.schemas import Task as TaskSchema, TaskCreate, TaskUpdate
from app.auth import get_current_active_user

router = APIRouter(prefix="/tasks/", tags=["tasks"])

@router.post("/", response_model=TaskSchema)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Verificar que la empresa existe
    company = db.query(Company).filter(Company.id == task.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verificar que el usuario asignado existe y pertenece a la empresa
    if task.assigned_to:
        assigned_user = db.query(User).filter(User.id == task.assigned_to).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")
        if assigned_user.company_id != task.company_id:
            raise HTTPException(status_code=400, detail="Assigned user must belong to the same company")
    
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        company_id=task.company_id,
        assigned_to=task.assigned_to,
        created_by=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskSchema])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Task)
    
    # Los usuarios solo pueden ver tareas de su empresa, excepto los admins
    if current_user.role != "admin":
        query = query.filter(Task.company_id == current_user.company_id)
    
    if company_id and company_id.strip():
        try:
            company_id_int = int(company_id)
            query = query.filter(Task.company_id == company_id_int)
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
        joinedload(Task.company),
        joinedload(Task.created_by_user)
    ).offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=TaskSchema)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = db.query(Task).options(
        joinedload(Task.assigned_user),
        joinedload(Task.company),
        joinedload(Task.created_by_user)
    ).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Los usuarios solo pueden ver tareas de su empresa, excepto los admins
    if current_user.role != "admin" and task.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return task

@router.put("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Los usuarios solo pueden actualizar tareas de su empresa, excepto los admins
    if current_user.role != "admin" and task.company_id != current_user.company_id:
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

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Los usuarios solo pueden eliminar tareas de su empresa, excepto los admins
    if current_user.role != "admin" and task.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
