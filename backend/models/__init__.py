"""
Modèles Pydantic pour Nümtema Agents Studio

Définitions type-safe pour:
- Agents et leurs configurations
- Workflows et leurs structures
- Exécutions et leur état
- Outils et leurs schémas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum


# =============================================================================
# ENUMS
# =============================================================================

class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NodeType(str, Enum):
    AGENT = "agent"
    TOOL = "tool"
    CONDITION = "condition"
    INPUT = "input"
    OUTPUT = "output"


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"


# =============================================================================
# AGENT MODELS
# =============================================================================

class AgentConfig(BaseModel):
    """Configuration d'un agent"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="")
    model_provider: LLMProvider = Field(default=LLMProvider.OPENAI)
    model_name: str = Field(default="gpt-4o")
    system_prompt: str = Field(...)
    tools: List[str] = Field(default_factory=list)
    max_retries: int = Field(default=3, ge=0, le=10)
    temperature: float = Field(default=0.7, ge=0, le=2)
    output_format: str = Field(default="text")  # text, json, yaml
    output_key: Optional[str] = Field(default=None)  # Pour state sharing


class AgentDefinition(BaseModel):
    """Définition complète d'un agent"""
    id: UUID = Field(default_factory=uuid4)
    config: AgentConfig
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[UUID] = None
    tags: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class AgentCreate(BaseModel):
    """Payload pour création d'agent"""
    config: AgentConfig
    tags: List[str] = Field(default_factory=list)


class AgentUpdate(BaseModel):
    """Payload pour mise à jour d'agent"""
    config: Optional[AgentConfig] = None
    tags: Optional[List[str]] = None


class AgentResponse(BaseModel):
    """Réponse API pour agent"""
    id: UUID
    config: AgentConfig
    version: str
    status: AgentStatus = AgentStatus.IDLE
    created_at: datetime
    updated_at: datetime
    tags: List[str] = Field(default_factory=list)


# =============================================================================
# WORKFLOW MODELS
# =============================================================================

class WorkflowNode(BaseModel):
    """Nœud dans un workflow"""
    id: UUID = Field(default_factory=uuid4)
    type: NodeType
    agent_id: Optional[UUID] = None  # Si type == AGENT
    agent_type: Optional[str] = None  # Type d'agent (research, writer, etc.)
    tool_name: Optional[str] = None  # Si type == TOOL
    config: Dict[str, Any] = Field(default_factory=dict)
    position: Dict[str, float] = Field(default_factory=lambda: {"x": 0, "y": 0})


class WorkflowEdge(BaseModel):
    """Connexion entre deux nœuds"""
    id: UUID = Field(default_factory=uuid4)
    source: UUID
    target: UUID
    condition: Optional[str] = None  # Condition pour transition
    label: Optional[str] = None


class WorkflowDefinition(BaseModel):
    """Définition complète d'un workflow"""
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1, max_length=100)
    description: str = ""
    version: str = "1.0.0"
    nodes: List[WorkflowNode] = Field(default_factory=list)
    edges: List[WorkflowEdge] = Field(default_factory=list)
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[UUID] = None
    
    class Config:
        from_attributes = True


class WorkflowCreate(BaseModel):
    """Payload pour création de workflow"""
    name: str
    description: str = ""
    nodes: List[WorkflowNode] = Field(default_factory=list)
    edges: List[WorkflowEdge] = Field(default_factory=list)
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)


class WorkflowResponse(BaseModel):
    """Réponse API pour workflow"""
    id: UUID
    name: str
    description: str
    version: str
    nodes: List[WorkflowNode]
    edges: List[WorkflowEdge]
    created_at: datetime
    updated_at: datetime


# =============================================================================
# EXECUTION MODELS
# =============================================================================

class ExecutionStep(BaseModel):
    """Étape d'exécution"""
    node_id: UUID
    node_name: str
    status: ExecutionStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: Optional[int] = None


class Execution(BaseModel):
    """Exécution d'un workflow"""
    id: UUID = Field(default_factory=uuid4)
    workflow_id: UUID
    status: ExecutionStatus = ExecutionStatus.PENDING
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    steps: List[ExecutionStep] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    user_id: Optional[UUID] = None
    
    class Config:
        from_attributes = True


class ExecutionRequest(BaseModel):
    """Requête d'exécution"""
    input_data: Dict[str, Any] = Field(default_factory=dict)
    async_mode: bool = True


class ExecutionResponse(BaseModel):
    """Réponse d'exécution"""
    execution_id: UUID
    status: ExecutionStatus
    message: str = ""


# =============================================================================
# TOOL MODELS
# =============================================================================

class ToolDefinition(BaseModel):
    """Définition d'un outil"""
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    version: str = "1.0.0"
    category: str  # search, calculation, file, api, database
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    requires_auth: bool = False
    rate_limit: Optional[Dict[str, int]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    """Appel d'outil"""
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """Résultat d'appel d'outil"""
    tool_name: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    duration_ms: int = 0


# =============================================================================
# SHARED STATE
# =============================================================================

class SharedState(BaseModel):
    """État partagé entre agents dans un workflow"""
    data: Dict[str, Any] = Field(default_factory=dict)
    history: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.history.append({
            "action": "set",
            "key": key,
            "timestamp": datetime.utcnow().isoformat()
        })


# Exports
__all__ = [
    # Enums
    "AgentStatus",
    "ExecutionStatus", 
    "NodeType",
    "LLMProvider",
    # Agent
    "AgentConfig",
    "AgentDefinition",
    "AgentCreate",
    "AgentUpdate",
    "AgentResponse",
    # Workflow
    "WorkflowNode",
    "WorkflowEdge",
    "WorkflowDefinition",
    "WorkflowCreate",
    "WorkflowResponse",
    # Execution
    "ExecutionStep",
    "Execution",
    "ExecutionRequest",
    "ExecutionResponse",
    # Tools
    "ToolDefinition",
    "ToolCall",
    "ToolResult",
    # State
    "SharedState",
]
