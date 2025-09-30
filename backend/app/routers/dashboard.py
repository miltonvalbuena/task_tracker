from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List
from datetime import datetime
from app.database import get_db
from app.models import Task, User, Company
from app.schemas import TaskStats, CompanyStats
from app.auth import get_current_active_user, require_admin

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=TaskStats)
def get_task_stats(
    company_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Los usuarios solo pueden ver estadísticas de su empresa, excepto los admins
    if current_user.role != "admin" and company_id != current_user.company_id:
        company_id = current_user.company_id
    
    query = db.query(Task)
    if company_id:
        query = query.filter(Task.company_id == company_id)
    
    total_tasks = query.count()
    pending_tasks = query.filter(Task.status == "pendiente").count()
    in_progress_tasks = query.filter(Task.status == "en_progreso").count()
    completed_tasks = query.filter(Task.status == "completada").count()
    
    # Tareas vencidas (pendientes o en progreso con fecha de vencimiento pasada)
    overdue_tasks = query.filter(
        and_(
            Task.status.in_(["pendiente", "en_progreso"]),
            Task.due_date < datetime.utcnow()
        )
    ).count()
    
    return TaskStats(
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks
    )

@router.get("/company-stats", response_model=List[CompanyStats])
def get_company_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    companies = db.query(Company).filter(Company.is_active == True).all()
    company_stats = []
    
    for company in companies:
        # Estadísticas de tareas para esta empresa
        tasks_query = db.query(Task).filter(Task.company_id == company.id)
        total_tasks = tasks_query.count()
        pending_tasks = tasks_query.filter(Task.status == "pendiente").count()
        in_progress_tasks = tasks_query.filter(Task.status == "en_progreso").count()
        completed_tasks = tasks_query.filter(Task.status == "completada").count()
        overdue_tasks = tasks_query.filter(
            and_(
                Task.status.in_(["pendiente", "en_progreso"]),
                Task.due_date < datetime.utcnow()
            )
        ).count()
        
        # Número total de usuarios
        total_users = db.query(User).filter(User.company_id == company.id).count()
        
        task_stats = TaskStats(
            total_tasks=total_tasks,
            pending_tasks=pending_tasks,
            in_progress_tasks=in_progress_tasks,
            completed_tasks=completed_tasks,
            overdue_tasks=overdue_tasks
        )
        
        company_stats.append(CompanyStats(
            company=company,
            task_stats=task_stats,
            total_users=total_users
        ))
    
    return company_stats

@router.get("/user-tasks/{user_id}")
def get_user_task_stats(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Verificar que el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Los usuarios solo pueden ver estadísticas de usuarios de su empresa, excepto los admins
    if current_user.role != "admin" and user.company_id != current_user.company_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Estadísticas de tareas asignadas al usuario
    tasks_query = db.query(Task).filter(Task.assigned_to == user_id)
    total_tasks = tasks_query.count()
    pending_tasks = tasks_query.filter(Task.status == "pendiente").count()
    in_progress_tasks = tasks_query.filter(Task.status == "en_progreso").count()
    completed_tasks = tasks_query.filter(Task.status == "completada").count()
    overdue_tasks = tasks_query.filter(
        and_(
            Task.status.in_(["pendiente", "en_progreso"]),
            Task.due_date < datetime.utcnow()
        )
    ).count()
    
    return TaskStats(
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks
    )
