from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TaskStatus(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

class TaskPriority(str, enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class FieldType(str, enum.Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    SELECT = "select"
    TEXTAREA = "textarea"

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Configuración de campos personalizados para esta empresa
    custom_fields_config = Column(JSON, default=list)  # Lista de campos personalizados
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    users = relationship("User", back_populates="company")
    tasks = relationship("Task", back_populates="company")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    company = relationship("Company", back_populates="users")
    assigned_tasks = relationship("Task", back_populates="assigned_user", foreign_keys="Task.assigned_to")
    created_tasks = relationship("Task", back_populates="created_by_user", foreign_keys="Task.created_by")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDIENTE)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIA)
    due_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Foreign Keys
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Campos personalizados dinámicos (JSON)
    custom_fields = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    company = relationship("Company", back_populates="tasks")
    assigned_user = relationship("User", back_populates="assigned_tasks", foreign_keys=[assigned_to])
    created_by_user = relationship("User", back_populates="created_tasks", foreign_keys=[created_by])