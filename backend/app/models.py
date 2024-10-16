from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel # type: ignore
from pydantic import Field as PydanticField # type: ignore
from sqlalchemy import ( # type: ignore
    JSON,   # el formato para pasar el token de acceso
    Column, # ahora las 5 columnas que va a tener el modelo  
    DateTime,
    PrimaryKeyConstraint,
    UniqueConstraint,
    func,
)
from sqlalchemy import ( # type: ignore
    Enum as SQLEnum, # enumerar las filas y columnas 
)
from sqlmodel import Field, Relationship, SQLModel # type: ignore

from app.core.graph.messages import ChatResponse


# Modelos para almacenar mensajes, tokens de acceso y contraseñas en la base de datos

class Message(SQLModel):  # tabla para almacenar mensajes de la aplicación
    message: str


# Modelo que almacena los tokens de acceso
 ## usado en la autenticación de usuarios
# El payload JSON incluye el token y el token es por defecto 'bearer'

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# payload de un Jason web token
 ## se almacena el campo 'sub' aunque no se use directamente

class TokenPayload(SQLModel):
    sub: int | None = None

# almacena el token de autenticación y una nueva contraseña 
 ## usuario solicita el cambio de contraseña
class NewPassword(SQLModel):  
    token: str
    new_password: str


# ===============USER========================

# datos basicos del usuario 
class UserBase(SQLModel):  
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None



class UserCreate(UserBase):  # Propiedad que se recibe cuando se crea la API
    password: str


# Crea nuevo usuario con los datos necesarios  
class UserCreateOpen(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None

class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Tabla ntermedia para enlazar miembros con uploads
## utilizada para manejar relaciones muchos-a-muchos
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    teams: list["Team"] = Relationship(back_populates="owner")
    skills: list["Skill"] = Relationship(back_populates="owner")
    uploads: list["Upload"] = Relationship(back_populates="owner")


# Si hacemos peticiones a la API aqui aparece lo que nos devolvera

class UserOut(UserBase):
    id: int


class UsersOut(SQLModel):
    data: list[UserOut]
    count: int


# ==============TEAM=========================

# Modelo que se usa para crear un equipo nuevo
# Hereda del modelo base y añade el campo de workflow (flujo de trabajo)
class TeamBase(SQLModel):
    name: str = PydanticField(pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    description: str | None = None

# crear un equipo nuevo
class TeamCreate(TeamBase):
    workflow: str

# actualizar la info de un equipo
class TeamUpdate(TeamBase):
    name: str | None = PydanticField(pattern=r"^[a-zA-Z0-9_-]{1,64}$", default=None)  # type: ignore[assignment]

# enumera que tipo de mensajes estan permitidos
class ChatMessageType(str, Enum):
    human = "human"
    ai = "ai"

# ejemplo de mensaje en un chat
## Cada mensaje tiene un tipo (human o ai) y un contenido
class ChatMessage(BaseModel):
    type: ChatMessageType
    content: str

# manera de interrupcion en el chat
class InterruptDecision(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"

# modelo que representa interrupcion en chat
class Interrupt(BaseModel):
    decision: InterruptDecision

# Modelo que representa un chat de equipo
# Contiene una lista de mensajes y una decisión de interrupción opcional
class TeamChat(BaseModel):
    messages: list[ChatMessage]
    interrupt_decision: InterruptDecision | None = None

# Modelo para representar un equipo en la base de datos
# Incluye relaciones con usuarios (owner), miembros, y threads
class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(regex=r"^[a-zA-Z0-9_-]{1,64}$", unique=True)  # Nombre único
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)  # Clave foránea a User
    owner: User | None = Relationship(back_populates="teams")  # Relación con el propietario (User)
    members: list["Member"] = Relationship(back_populates="belongs", sa_relationship_kwargs={"cascade": "delete"})  # Relación con los miembros del equipo
    workflow: str
    threads: list["Thread"] = Relationship(back_populates="team", sa_relationship_kwargs={"cascade": "delete"})  # Relación con los threads



# Modelo que sirve para devolver información del equipo al hacer peticiones a la API
class TeamOut(TeamBase):
    id: int
    owner_id: int
    workflow: str


class TeamsOut(SQLModel):
    data: list[TeamOut]
    count: int


# =============Threads===================

# Creamos el thread y va a ser un string
  ## le añadimos la caapcidad de almacenar modificaciones
# Le añadimos una config inicial: id, updated_At,team_id,team,checkpoints,writes
class ThreadBase(SQLModel):
    query: str


class ThreadCreate(ThreadBase):
    pass


class ThreadUpdate(ThreadBase):
    query: str | None = None  # type: ignore[assignment]
    updated_at: datetime | None = None


class Thread(ThreadBase, table=True):
    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=func.now(),
            onupdate=func.now(),
            server_default=func.now(),
        )
    )
    team_id: int | None = Field(default=None, foreign_key="team.id", nullable=False)
    team: Team | None = Relationship(back_populates="threads")
    checkpoints: list["Checkpoint"] = Relationship(
        back_populates="thread", sa_relationship_kwargs={"cascade": "delete"}
    )
    writes: list["Write"] = Relationship(
        back_populates="thread", sa_relationship_kwargs={"cascade": "delete"}
    )


# Si hacemos peticion a la Api nos devuelve esto
class ThreadOut(SQLModel):
    id: UUID
    query: str
    updated_at: datetime


class ThreadRead(ThreadOut):
    messages: list[ChatResponse]


class ThreadsOut(SQLModel):
    data: list[ThreadOut]
    count: int


# ==============MEMBER=========================

# Creamos tabla para los miembros 
class MemberSkillsLink(SQLModel, table=True):
    member_id: int | None = Field(
        default=None, foreign_key="member.id", primary_key=True
    )
    skill_id: int | None = Field(default=None, foreign_key="skill.id", primary_key=True)


class MemberUploadsLink(SQLModel, table=True):
    member_id: int | None = Field(
        default=None, foreign_key="member.id", primary_key=True
    )
    upload_id: int | None = Field(
        default=None, foreign_key="upload.id", primary_key=True
    )


class MemberBase(SQLModel):
    name: str = PydanticField(pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    backstory: str | None = None
    role: str
    type: str  # one of: leader, worker, freelancer
    owner_of: int | None = None
    position_x: float
    position_y: float
    source: int | None = None
    provider: str = "ChatOpenAI"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    interrupt: bool = False


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
    name: str | None = PydanticField(pattern=r"^[a-zA-Z0-9_-]{1,64}$", default=None)  # type: ignore[assignment]
    backstory: str | None = None
    role: str | None = None  # type: ignore[assignment]
    type: str | None = None  # type: ignore[assignment]
    belongs_to: int | None = None
    position_x: float | None = None  # type: ignore[assignment]
    position_y: float | None = None  # type: ignore[assignment]
    skills: list["Skill"] | None = None
    uploads: list["Upload"] | None = None
    provider: str | None = None  # type: ignore[assignment]
    model: str | None = None  # type: ignore[assignment]
    temperature: float | None = None  # type: ignore[assignment]
    interrupt: bool | None = None  # type: ignore[assignment]


class Member(MemberBase, table=True):
    __table_args__ = (
        UniqueConstraint("name", "belongs_to", name="unique_team_and_name"),
    )
    id: int | None = Field(default=None, primary_key=True)
    belongs_to: int | None = Field(default=None, foreign_key="team.id", nullable=False)
    belongs: Team | None = Relationship(back_populates="members")
    skills: list["Skill"] = Relationship(
        back_populates="members",
        link_model=MemberSkillsLink,
    )
    uploads: list["Upload"] = Relationship(
        back_populates="members",
        link_model=MemberUploadsLink,
    )


class MemberOut(MemberBase):
    id: int
    belongs_to: int
    owner_of: int | None
    skills: list["Skill"]
    uploads: list["Upload"]


class MembersOut(SQLModel):
    data: list[MemberOut]
    count: int


# ===============SKILL========================


class SkillBase(SQLModel):
    name: str
    description: str
    managed: bool = False
    tool_definition: dict[str, Any] | None = Field(
        default_factory=dict, sa_column=Column(JSON)
    )


class SkillCreate(SkillBase):
    tool_definition: dict[str, Any]  # Tool definition is required if not managed
    managed: bool = Field(default=False, const=False)  # Managed must be False


class SkillUpdate(SkillBase):
    name: str | None = None  # type: ignore[assignment]
    description: str | None = None  # type: ignore[assignment]
    managed: bool | None = None  # type: ignore[assignment]
    tool_definition: dict[str, Any] | None = None


class Skill(SkillBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    members: list["Member"] = Relationship(
        back_populates="skills",
        link_model=MemberSkillsLink,
    )
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="skills")


class SkillsOut(SQLModel):
    data: list["SkillOut"]
    count: int


class SkillOut(SkillBase):
    id: int


class ToolDefinitionValidate(SQLModel):
    tool_definition: dict[str, Any]


# ==============CHECKPOINT=====================


class Checkpoint(SQLModel, table=True):
    __tablename__ = "checkpoints"
    __table_args__ = (PrimaryKeyConstraint("thread_id", "thread_ts"),)
    thread_id: UUID = Field(foreign_key="thread.id", primary_key=True)
    thread_ts: UUID = Field(primary_key=True)
    parent_ts: UUID | None
    checkpoint: bytes
    metadata_: bytes = Field(sa_column_kwargs={"name": "metadata"})
    thread: Thread = Relationship(back_populates="checkpoints")
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=func.now(),
            server_default=func.now(),
        )
    )


class CheckpointOut(SQLModel):
    thread_id: UUID
    thread_ts: UUID
    checkpoint: bytes
    created_at: datetime


class Write(SQLModel, table=True):
    __tablename__ = "writes"
    __table_args__ = (PrimaryKeyConstraint("thread_id", "thread_ts", "task_id", "idx"),)
    thread_id: UUID = Field(foreign_key="thread.id", primary_key=True)
    thread_ts: UUID = Field(primary_key=True)
    task_id: UUID = Field(primary_key=True)
    idx: int = Field(primary_key=True)
    channel: str
    value: bytes
    thread: Thread = Relationship(back_populates="writes")


# ==============Uploads=====================


class UploadBase(SQLModel):
    name: str
    description: str


class UploadCreate(UploadBase):
    pass


class UploadUpdate(UploadBase):
    name: str | None = None  # type: ignore[assignment]
    description: str | None = None  # type: ignore[assignment]
    last_modified: datetime


class UploadStatus(str, Enum):
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"


class Upload(UploadBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="uploads")
    members: list["Member"] = Relationship(
        back_populates="uploads",
        link_model=MemberUploadsLink,
    )
    last_modified: datetime = Field(default_factory=lambda: datetime.now())
    status: UploadStatus = Field(
        sa_column=Column(SQLEnum(UploadStatus), nullable=False)
    )


class UploadOut(UploadBase):
    id: int
    name: str
    last_modified: datetime
    status: UploadStatus


class UploadsOut(SQLModel):
    data: list[UploadOut]
    count: int
