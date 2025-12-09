"""
API REST pour Nümtema Agents Studio

Endpoints pour:
- Gestion des agents
- Gestion des workflows  
- Exécutions
- Outils
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime
import asyncio

from models import (
    AgentDefinition, AgentCreate, AgentUpdate, AgentResponse, AgentStatus,
    WorkflowDefinition, WorkflowCreate, WorkflowResponse,
    ExecutionRequest, ExecutionResponse, Execution, ExecutionStatus,
    ToolDefinition,
)
from workflows import workflow_engine, create_workflow_from_template, WORKFLOW_TEMPLATES
from tools import tool_registry
from agents import AGENT_REGISTRY, AgentBuilder


# =============================================================================
# APPLICATION
# =============================================================================

app = FastAPI(
    title="Nümtema Agents Studio API",
    description="Studio d'Agents IA - API REST basée sur PocketFlow",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# IN-MEMORY STORAGE (à remplacer par PostgreSQL en production)
# =============================================================================

agents_db: Dict[str, AgentDefinition] = {}
workflows_db: Dict[str, WorkflowDefinition] = {}
executions_db: Dict[str, Execution] = {}


# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/")
async def root():
    """Point d'entrée racine"""
    return {
        "name": "Nümtema Agents Studio",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# =============================================================================
# ENDPOINTS AGENTS
# =============================================================================

@app.post("/api/v1/agents", response_model=AgentResponse, tags=["Agents"])
async def create_agent(data: AgentCreate):
    """Crée un nouvel agent"""
    agent = AgentDefinition(
        config=data.config,
        tags=data.tags
    )
    agents_db[str(agent.id)] = agent
    return AgentResponse(
        id=agent.id,
        config=agent.config,
        version=agent.version,
        created_at=agent.created_at,
        updated_at=agent.updated_at,
        tags=agent.tags
    )


@app.get("/api/v1/agents", response_model=List[AgentResponse], tags=["Agents"])
async def list_agents(
    tag: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """Liste tous les agents"""
    agents = list(agents_db.values())
    
    if tag:
        agents = [a for a in agents if tag in a.tags]
    
    agents = agents[offset:offset + limit]
    
    return [
        AgentResponse(
            id=a.id,
            config=a.config,
            version=a.version,
            created_at=a.created_at,
            updated_at=a.updated_at,
            tags=a.tags
        )
        for a in agents
    ]


@app.get("/api/v1/agents/{agent_id}", response_model=AgentResponse, tags=["Agents"])
async def get_agent(agent_id: str):
    """Récupère un agent par son ID"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    agent = agents_db[agent_id]
    return AgentResponse(
        id=agent.id,
        config=agent.config,
        version=agent.version,
        created_at=agent.created_at,
        updated_at=agent.updated_at,
        tags=agent.tags
    )


@app.put("/api/v1/agents/{agent_id}", response_model=AgentResponse, tags=["Agents"])
async def update_agent(agent_id: str, data: AgentUpdate):
    """Met à jour un agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    agent = agents_db[agent_id]
    
    if data.config:
        agent.config = data.config
    if data.tags is not None:
        agent.tags = data.tags
    
    agent.updated_at = datetime.utcnow()
    
    return AgentResponse(
        id=agent.id,
        config=agent.config,
        version=agent.version,
        created_at=agent.created_at,
        updated_at=agent.updated_at,
        tags=agent.tags
    )


@app.delete("/api/v1/agents/{agent_id}", tags=["Agents"])
async def delete_agent(agent_id: str):
    """Supprime un agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    del agents_db[agent_id]
    return {"status": "deleted", "id": agent_id}


@app.get("/api/v1/agents/types", tags=["Agents"])
async def list_agent_types():
    """Liste les types d'agents disponibles"""
    return {
        "types": list(AGENT_REGISTRY.keys()),
        "count": len(AGENT_REGISTRY)
    }


# =============================================================================
# ENDPOINTS WORKFLOWS
# =============================================================================

@app.post("/api/v1/workflows", response_model=WorkflowResponse, tags=["Workflows"])
async def create_workflow(data: WorkflowCreate):
    """Crée un nouveau workflow"""
    workflow = WorkflowDefinition(
        name=data.name,
        description=data.description,
        nodes=data.nodes,
        edges=data.edges,
        input_schema=data.input_schema,
        output_schema=data.output_schema
    )
    workflows_db[str(workflow.id)] = workflow
    return WorkflowResponse(
        id=workflow.id,
        name=workflow.name,
        description=workflow.description,
        version=workflow.version,
        nodes=workflow.nodes,
        edges=workflow.edges,
        created_at=workflow.created_at,
        updated_at=workflow.updated_at
    )


@app.get("/api/v1/workflows", response_model=List[WorkflowResponse], tags=["Workflows"])
async def list_workflows(limit: int = 100, offset: int = 0):
    """Liste tous les workflows"""
    workflows = list(workflows_db.values())[offset:offset + limit]
    return [
        WorkflowResponse(
            id=w.id,
            name=w.name,
            description=w.description,
            version=w.version,
            nodes=w.nodes,
            edges=w.edges,
            created_at=w.created_at,
            updated_at=w.updated_at
        )
        for w in workflows
    ]


@app.get("/api/v1/workflows/{workflow_id}", response_model=WorkflowResponse, tags=["Workflows"])
async def get_workflow(workflow_id: str):
    """Récupère un workflow par son ID"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow non trouvé")
    
    w = workflows_db[workflow_id]
    return WorkflowResponse(
        id=w.id,
        name=w.name,
        description=w.description,
        version=w.version,
        nodes=w.nodes,
        edges=w.edges,
        created_at=w.created_at,
        updated_at=w.updated_at
    )


@app.delete("/api/v1/workflows/{workflow_id}", tags=["Workflows"])
async def delete_workflow(workflow_id: str):
    """Supprime un workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow non trouvé")
    
    del workflows_db[workflow_id]
    return {"status": "deleted", "id": workflow_id}


@app.get("/api/v1/workflows/templates", tags=["Workflows"])
async def list_workflow_templates():
    """Liste les templates de workflows disponibles"""
    templates = []
    for name, factory in WORKFLOW_TEMPLATES.items():
        workflow = factory()
        templates.append({
            "name": name,
            "display_name": workflow.name,
            "description": workflow.description,
            "nodes_count": len(workflow.nodes),
            "edges_count": len(workflow.edges)
        })
    return {"templates": templates}


@app.post("/api/v1/workflows/from-template/{template_name}", response_model=WorkflowResponse, tags=["Workflows"])
async def create_workflow_from_template_endpoint(template_name: str):
    """Crée un workflow à partir d'un template"""
    try:
        workflow = create_workflow_from_template(template_name)
        workflows_db[str(workflow.id)] = workflow
        return WorkflowResponse(
            id=workflow.id,
            name=workflow.name,
            description=workflow.description,
            version=workflow.version,
            nodes=workflow.nodes,
            edges=workflow.edges,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =============================================================================
# ENDPOINTS EXECUTIONS
# =============================================================================

async def run_workflow_background(
    execution_id: str,
    workflow: WorkflowDefinition,
    input_data: Dict
):
    """Exécute un workflow en arrière-plan"""
    execution = executions_db[execution_id]
    
    try:
        result = await workflow_engine.run_async(workflow, input_data)
        execution.status = ExecutionStatus.COMPLETED
        execution.output_data = result.output_data
    except Exception as e:
        execution.status = ExecutionStatus.FAILED
        execution.error = str(e)
    finally:
        execution.completed_at = datetime.utcnow()


@app.post("/api/v1/workflows/{workflow_id}/execute", response_model=ExecutionResponse, tags=["Executions"])
async def execute_workflow(
    workflow_id: str,
    data: ExecutionRequest,
    background_tasks: BackgroundTasks
):
    """Lance l'exécution d'un workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow non trouvé")
    
    workflow = workflows_db[workflow_id]
    
    # Créer l'exécution
    execution = Execution(
        workflow_id=UUID(workflow_id),
        input_data=data.input_data,
        status=ExecutionStatus.PENDING if data.async_mode else ExecutionStatus.RUNNING
    )
    executions_db[str(execution.id)] = execution
    
    if data.async_mode:
        # Exécution asynchrone en arrière-plan
        execution.status = ExecutionStatus.RUNNING
        background_tasks.add_task(
            run_workflow_background,
            str(execution.id),
            workflow,
            data.input_data
        )
        return ExecutionResponse(
            execution_id=execution.id,
            status=execution.status,
            message="Exécution démarrée en arrière-plan"
        )
    else:
        # Exécution synchrone
        result = workflow_engine.run(workflow, data.input_data)
        execution.status = result.status
        execution.output_data = result.output_data
        execution.error = result.error
        execution.completed_at = datetime.utcnow()
        
        return ExecutionResponse(
            execution_id=execution.id,
            status=execution.status,
            message="Exécution terminée"
        )


@app.get("/api/v1/executions/{execution_id}", tags=["Executions"])
async def get_execution(execution_id: str):
    """Récupère le statut d'une exécution"""
    if execution_id not in executions_db:
        raise HTTPException(status_code=404, detail="Exécution non trouvée")
    
    execution = executions_db[execution_id]
    return {
        "id": str(execution.id),
        "workflow_id": str(execution.workflow_id),
        "status": execution.status,
        "input_data": execution.input_data,
        "output_data": execution.output_data,
        "error": execution.error,
        "started_at": execution.started_at.isoformat(),
        "completed_at": execution.completed_at.isoformat() if execution.completed_at else None
    }


@app.get("/api/v1/executions", tags=["Executions"])
async def list_executions(
    workflow_id: Optional[str] = None,
    status: Optional[ExecutionStatus] = None,
    limit: int = 100
):
    """Liste les exécutions"""
    executions = list(executions_db.values())
    
    if workflow_id:
        executions = [e for e in executions if str(e.workflow_id) == workflow_id]
    
    if status:
        executions = [e for e in executions if e.status == status]
    
    executions = executions[:limit]
    
    return {
        "executions": [
            {
                "id": str(e.id),
                "workflow_id": str(e.workflow_id),
                "status": e.status,
                "started_at": e.started_at.isoformat(),
                "completed_at": e.completed_at.isoformat() if e.completed_at else None
            }
            for e in executions
        ],
        "count": len(executions)
    }


# =============================================================================
# ENDPOINTS TOOLS
# =============================================================================

@app.get("/api/v1/tools", tags=["Tools"])
async def list_tools(category: Optional[str] = None):
    """Liste les outils disponibles"""
    tools = tool_registry.list_tools(category)
    return {"tools": tools, "count": len(tools)}


@app.post("/api/v1/tools/{tool_name}/execute", tags=["Tools"])
async def execute_tool(tool_name: str, arguments: Dict[str, Any] = {}):
    """Exécute un outil"""
    try:
        result = tool_registry.execute(tool_name, **arguments)
        return {"tool": tool_name, "result": result, "success": True}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ENDPOINTS AGENT BUILDER
# =============================================================================

class BuilderRequest(BaseModel):
    """Requête pour l'Agent Builder"""
    request: str
    context: Optional[Dict[str, Any]] = None


@app.post("/api/v1/builder/execute", tags=["Builder"])
async def execute_builder(data: BuilderRequest):
    """Exécute l'Agent Builder pour gérer les agents et workflows via MCP Tools"""
    try:
        # Créer une instance d'AgentBuilder
        builder = AgentBuilder()
        
        # Injecter le registre des outils
        builder.register_tool_registry(tool_registry)
        
        # Préparer le contexte partagé
        shared = {
            "builder_request": data.request,
            "agents_list": list(agents_db.values()),
            "workflows_list": list(workflows_db.values()),
            "builder_context": data.context or {}
        }
        
        # Exécuter le builder
        action = builder.run(shared)
        
        return {
            "status": "executed",
            "action": shared.get("last_action"),
            "result": shared.get("builder_result"),
            "error": shared.get("builder_error")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/builder/capabilities", tags=["Builder"])
async def get_builder_capabilities():
    """Retourne les capacités de l'Agent Builder"""
    return {
        "name": "Agent Builder",
        "description": "Agent spécialisé en création et gestion d'agents et workflows",
        "capabilities": [
            "create_agent",
            "update_agent",
            "delete_agent",
            "list_agents",
            "get_agent",
            "create_workflow",
            "update_workflow",
            "delete_workflow",
            "list_workflows",
            "get_workflow"
        ],
        "input_format": "natural language request",
        "output_format": "JSON with action and parameters"
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Point d'entrée pour lancer le serveur"""
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
