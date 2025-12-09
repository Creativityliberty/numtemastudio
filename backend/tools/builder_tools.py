"""
Builder Tools - Outils MCP pour gérer les agents et workflows

Outils spécialisés pour l'Agent Builder:
- create_agent: Crée un nouvel agent
- update_agent: Met à jour un agent
- delete_agent: Supprime un agent
- list_agents: Liste les agents
- get_agent: Récupère les détails d'un agent
- create_workflow: Crée un workflow
- update_workflow: Met à jour un workflow
- delete_workflow: Supprime un workflow
- list_workflows: Liste les workflows
- get_workflow: Récupère les détails d'un workflow
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import uuid4
import json


# =============================================================================
# IN-MEMORY STORAGE (à remplacer par PostgreSQL en production)
# =============================================================================

agents_storage: Dict[str, Dict[str, Any]] = {}
workflows_storage: Dict[str, Dict[str, Any]] = {}


# =============================================================================
# AGENT TOOLS
# =============================================================================

def create_agent(
    name: str,
    description: str = "",
    agent_type: str = "custom",
    config: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Crée un nouvel agent
    
    Args:
        name: Nom de l'agent
        description: Description de l'agent
        agent_type: Type d'agent (research, writer, reviewer, coder, custom)
        config: Configuration de l'agent
        tags: Tags pour catégoriser l'agent
    
    Returns:
        Dictionnaire avec les détails de l'agent créé
    """
    try:
        agent_id = f"agent_{name.lower().replace(' ', '_')}_{str(uuid4())[:8]}"
        
        agent = {
            "id": agent_id,
            "name": name,
            "description": description,
            "type": agent_type,
            "config": config or {
                "model_name": "gpt-4o",
                "temperature": 0.7,
                "max_retries": 3
            },
            "tags": tags or [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        agents_storage[agent_id] = agent
        
        return {
            "success": True,
            "status": "created",
            "agent": agent,
            "message": f"Agent '{name}' créé avec succès"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors de la création de l'agent: {str(e)}"
        }


def update_agent(
    agent_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Met à jour un agent existant
    
    Args:
        agent_id: ID de l'agent à mettre à jour
        name: Nouveau nom (optionnel)
        description: Nouvelle description (optionnel)
        config: Nouvelle configuration (optionnel)
        tags: Nouveaux tags (optionnel)
    
    Returns:
        Dictionnaire avec les détails de l'agent mis à jour
    """
    try:
        if agent_id not in agents_storage:
            return {
                "success": False,
                "error": f"Agent non trouvé: {agent_id}",
                "message": f"L'agent '{agent_id}' n'existe pas"
            }
        
        agent = agents_storage[agent_id]
        
        if name is not None:
            agent["name"] = name
        if description is not None:
            agent["description"] = description
        if config is not None:
            agent["config"].update(config)
        if tags is not None:
            agent["tags"] = tags
        
        agent["updated_at"] = datetime.utcnow().isoformat()
        
        return {
            "success": True,
            "status": "updated",
            "agent": agent,
            "message": f"Agent '{agent_id}' mis à jour avec succès"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors de la mise à jour: {str(e)}"
        }


def delete_agent(agent_id: str) -> Dict[str, Any]:
    """
    Supprime un agent
    
    Args:
        agent_id: ID de l'agent à supprimer
    
    Returns:
        Dictionnaire avec le statut de suppression
    """
    try:
        if agent_id not in agents_storage:
            return {
                "success": False,
                "error": f"Agent non trouvé: {agent_id}",
                "message": f"L'agent '{agent_id}' n'existe pas"
            }
        
        agent = agents_storage.pop(agent_id)
        
        return {
            "success": True,
            "status": "deleted",
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "message": f"Agent '{agent['name']}' supprimé avec succès"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors de la suppression: {str(e)}"
        }


def list_agents(
    agent_type: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Liste les agents disponibles
    
    Args:
        agent_type: Filtrer par type d'agent (optionnel)
        tag: Filtrer par tag (optionnel)
        limit: Nombre maximum d'agents à retourner
        offset: Décalage pour la pagination
    
    Returns:
        Dictionnaire avec la liste des agents
    """
    try:
        agents = list(agents_storage.values())
        
        if agent_type:
            agents = [a for a in agents if a["type"] == agent_type]
        
        if tag:
            agents = [a for a in agents if tag in a["tags"]]
        
        total = len(agents)
        agents = agents[offset:offset + limit]
        
        return {
            "success": True,
            "status": "listed",
            "agents": agents,
            "total": total,
            "count": len(agents),
            "offset": offset,
            "limit": limit,
            "message": f"{len(agents)} agent(s) trouvé(s)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors du listage: {str(e)}"
        }


def get_agent(agent_id: str) -> Dict[str, Any]:
    """
    Récupère les détails d'un agent
    
    Args:
        agent_id: ID de l'agent
    
    Returns:
        Dictionnaire avec les détails de l'agent
    """
    try:
        if agent_id not in agents_storage:
            return {
                "success": False,
                "error": f"Agent non trouvé: {agent_id}",
                "message": f"L'agent '{agent_id}' n'existe pas"
            }
        
        agent = agents_storage[agent_id]
        
        return {
            "success": True,
            "status": "retrieved",
            "agent": agent,
            "message": f"Agent '{agent['name']}' récupéré avec succès"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors de la récupération: {str(e)}"
        }


# =============================================================================
# WORKFLOW TOOLS
# =============================================================================

def create_workflow(
    name: str,
    description: str = "",
    nodes: Optional[List[Dict[str, Any]]] = None,
    edges: Optional[List[Dict[str, Any]]] = None,
    input_schema: Optional[Dict[str, Any]] = None,
    output_schema: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Crée un nouveau workflow
    
    Args:
        name: Nom du workflow
        description: Description du workflow
        nodes: Liste des nœuds du workflow
        edges: Liste des connexions entre nœuds
        input_schema: Schéma d'entrée du workflow
        output_schema: Schéma de sortie du workflow
    
    Returns:
        Dictionnaire avec les détails du workflow créé
    """
    try:
        workflow_id = f"workflow_{name.lower().replace(' ', '_')}_{str(uuid4())[:8]}"
        
        workflow = {
            "id": workflow_id,
            "name": name,
            "description": description,
            "nodes": nodes or [],
            "edges": edges or [],
            "input_schema": input_schema or {},
            "output_schema": output_schema or {},
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "status": "active",
            "version": 1
        }
        
        workflows_storage[workflow_id] = workflow
        
        return {
            "success": True,
            "status": "created",
            "workflow": workflow,
            "message": f"Workflow '{name}' créé avec succès"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors de la création du workflow: {str(e)}"
        }


def update_workflow(
    workflow_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    nodes: Optional[List[Dict[str, Any]]] = None,
    edges: Optional[List[Dict[str, Any]]] = None,
    input_schema: Optional[Dict[str, Any]] = None,
    output_schema: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Met à jour un workflow existant
    
    Args:
        workflow_id: ID du workflow à mettre à jour
        name: Nouveau nom (optionnel)
        description: Nouvelle description (optionnel)
        nodes: Nouveaux nœuds (optionnel)
        edges: Nouvelles connexions (optionnel)
        input_schema: Nouveau schéma d'entrée (optionnel)
        output_schema: Nouveau schéma de sortie (optionnel)
    
    Returns:
        Dictionnaire avec les détails du workflow mis à jour
    """
    try:
        if workflow_id not in workflows_storage:
            return {
                "success": False,
                "error": f"Workflow non trouvé: {workflow_id}",
                "message": f"Le workflow '{workflow_id}' n'existe pas"
            }
        
        workflow = workflows_storage[workflow_id]
        
        if name is not None:
            workflow["name"] = name
        if description is not None:
            workflow["description"] = description
        if nodes is not None:
            workflow["nodes"] = nodes
        if edges is not None:
            workflow["edges"] = edges
        if input_schema is not None:
            workflow["input_schema"] = input_schema
        if output_schema is not None:
            workflow["output_schema"] = output_schema
        
        workflow["updated_at"] = datetime.utcnow().isoformat()
        workflow["version"] += 1
        
        return {
            "success": True,
            "status": "updated",
            "workflow": workflow,
            "message": f"Workflow '{workflow_id}' mis à jour avec succès"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors de la mise à jour: {str(e)}"
        }


def delete_workflow(workflow_id: str) -> Dict[str, Any]:
    """
    Supprime un workflow
    
    Args:
        workflow_id: ID du workflow à supprimer
    
    Returns:
        Dictionnaire avec le statut de suppression
    """
    try:
        if workflow_id not in workflows_storage:
            return {
                "success": False,
                "error": f"Workflow non trouvé: {workflow_id}",
                "message": f"Le workflow '{workflow_id}' n'existe pas"
            }
        
        workflow = workflows_storage.pop(workflow_id)
        
        return {
            "success": True,
            "status": "deleted",
            "workflow_id": workflow_id,
            "workflow_name": workflow["name"],
            "message": f"Workflow '{workflow['name']}' supprimé avec succès"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors de la suppression: {str(e)}"
        }


def list_workflows(
    limit: int = 100,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Liste les workflows disponibles
    
    Args:
        limit: Nombre maximum de workflows à retourner
        offset: Décalage pour la pagination
    
    Returns:
        Dictionnaire avec la liste des workflows
    """
    try:
        workflows = list(workflows_storage.values())
        total = len(workflows)
        workflows = workflows[offset:offset + limit]
        
        return {
            "success": True,
            "status": "listed",
            "workflows": workflows,
            "total": total,
            "count": len(workflows),
            "offset": offset,
            "limit": limit,
            "message": f"{len(workflows)} workflow(s) trouvé(s)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors du listage: {str(e)}"
        }


def get_workflow(workflow_id: str) -> Dict[str, Any]:
    """
    Récupère les détails d'un workflow
    
    Args:
        workflow_id: ID du workflow
    
    Returns:
        Dictionnaire avec les détails du workflow
    """
    try:
        if workflow_id not in workflows_storage:
            return {
                "success": False,
                "error": f"Workflow non trouvé: {workflow_id}",
                "message": f"Le workflow '{workflow_id}' n'existe pas"
            }
        
        workflow = workflows_storage[workflow_id]
        
        return {
            "success": True,
            "status": "retrieved",
            "workflow": workflow,
            "message": f"Workflow '{workflow['name']}' récupéré avec succès"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Erreur lors de la récupération: {str(e)}"
        }


# =============================================================================
# TOOL REGISTRY INTEGRATION
# =============================================================================

def register_builder_tools(tool_registry):
    """
    Enregistre tous les builder tools dans le registre global
    
    Args:
        tool_registry: Instance du registre des outils
    """
    
    # Agent Tools
    tool_registry.register(
        name="create_agent",
        func=create_agent,
        description="Crée un nouvel agent avec configuration",
        category="builder",
        input_schema={
            "name": "string",
            "description": "string",
            "agent_type": "string",
            "config": "object",
            "tags": "array"
        },
        output_schema={
            "success": "boolean",
            "status": "string",
            "agent": "object"
        }
    )
    
    tool_registry.register(
        name="update_agent",
        func=update_agent,
        description="Met à jour un agent existant",
        category="builder",
        input_schema={
            "agent_id": "string",
            "name": "string",
            "description": "string",
            "config": "object",
            "tags": "array"
        },
        output_schema={
            "success": "boolean",
            "status": "string",
            "agent": "object"
        }
    )
    
    tool_registry.register(
        name="delete_agent",
        func=delete_agent,
        description="Supprime un agent",
        category="builder",
        input_schema={
            "agent_id": "string"
        },
        output_schema={
            "success": "boolean",
            "status": "string"
        }
    )
    
    tool_registry.register(
        name="list_agents",
        func=list_agents,
        description="Liste tous les agents disponibles",
        category="builder",
        input_schema={
            "agent_type": "string",
            "tag": "string",
            "limit": "integer",
            "offset": "integer"
        },
        output_schema={
            "success": "boolean",
            "agents": "array",
            "total": "integer"
        }
    )
    
    tool_registry.register(
        name="get_agent",
        func=get_agent,
        description="Récupère les détails d'un agent",
        category="builder",
        input_schema={
            "agent_id": "string"
        },
        output_schema={
            "success": "boolean",
            "agent": "object"
        }
    )
    
    # Workflow Tools
    tool_registry.register(
        name="create_workflow",
        func=create_workflow,
        description="Crée un nouveau workflow",
        category="builder",
        input_schema={
            "name": "string",
            "description": "string",
            "nodes": "array",
            "edges": "array",
            "input_schema": "object",
            "output_schema": "object"
        },
        output_schema={
            "success": "boolean",
            "status": "string",
            "workflow": "object"
        }
    )
    
    tool_registry.register(
        name="update_workflow",
        func=update_workflow,
        description="Met à jour un workflow existant",
        category="builder",
        input_schema={
            "workflow_id": "string",
            "name": "string",
            "description": "string",
            "nodes": "array",
            "edges": "array",
            "input_schema": "object",
            "output_schema": "object"
        },
        output_schema={
            "success": "boolean",
            "status": "string",
            "workflow": "object"
        }
    )
    
    tool_registry.register(
        name="delete_workflow",
        func=delete_workflow,
        description="Supprime un workflow",
        category="builder",
        input_schema={
            "workflow_id": "string"
        },
        output_schema={
            "success": "boolean",
            "status": "string"
        }
    )
    
    tool_registry.register(
        name="list_workflows",
        func=list_workflows,
        description="Liste tous les workflows disponibles",
        category="builder",
        input_schema={
            "limit": "integer",
            "offset": "integer"
        },
        output_schema={
            "success": "boolean",
            "workflows": "array",
            "total": "integer"
        }
    )
    
    tool_registry.register(
        name="get_workflow",
        func=get_workflow,
        description="Récupère les détails d'un workflow",
        category="builder",
        input_schema={
            "workflow_id": "string"
        },
        output_schema={
            "success": "boolean",
            "workflow": "object"
        }
    )


__all__ = [
    "create_agent",
    "update_agent",
    "delete_agent",
    "list_agents",
    "get_agent",
    "create_workflow",
    "update_workflow",
    "delete_workflow",
    "list_workflows",
    "get_workflow",
    "register_builder_tools",
    "agents_storage",
    "workflows_storage"
]
