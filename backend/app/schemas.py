from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import TaskStatus, TaskPriority, UserRole, FieldType

# ARL Schemas
class ARLBase(BaseModel):
    name: str
    description: Optional[str] = None

class ARLCreate(ARLBase):
    pass

class ARLUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ARL(ARLBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Client Schemas
class ClientBase(BaseModel):
    name: str
    nit: Optional[str] = None
    description: Optional[str] = None
    arl_id: int

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    nit: Optional[str] = None
    description: Optional[str] = None
    arl_id: Optional[int] = None
    is_active: Optional[bool] = None

class Client(ClientBase):
    id: int
    is_active: bool
    custom_fields_config: Optional[List[Dict[str, Any]]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    arl: ARL  # Incluir información de la ARL
    
    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str
    client_id: int

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    client_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    client: Optional[Client] = None
    
    class Config:
        from_attributes = True

# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDIENTE
    priority: TaskPriority = TaskPriority.MEDIA
    due_date: Optional[datetime] = None
    custom_fields: Optional[dict] = {}

class TaskCreate(TaskBase):
    assigned_to: Optional[int] = None
    client_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    custom_fields: Optional[dict] = None

class Task(TaskBase):
    id: int
    client_id: int
    assigned_to: Optional[int] = None
    created_by: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    client: Client
    assigned_user: Optional[User] = None
    created_by_user: User
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# Dashboard Schemas
class TaskStats(BaseModel):
    total_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int
    overdue_tasks: int

class ClientStats(BaseModel):
    client: Client
    task_stats: TaskStats
    total_users: int

# Custom Field Schemas
class CustomFieldConfig(BaseModel):
    name: str
    label: str
    field_type: FieldType
    required: bool = False
    options: Optional[List[str]] = None  # Para campos SELECT
    placeholder: Optional[str] = None
    help_text: Optional[str] = None

class ClientConfigUpdate(BaseModel):
    custom_fields_config: List[CustomFieldConfig]
