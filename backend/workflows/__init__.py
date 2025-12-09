"""
Moteur de Workflow pour Nümtema Agents Studio

Responsable de:
- Construction de flows PocketFlow à partir de définitions
- Exécution de workflows
- Templates de workflows prédéfinis
"""

from typing import Dict, Type, Optional, Any, List
from uuid import UUID
from datetime import datetime

from pocketflow import Flow, Node
from models import (
    WorkflowDefinition, 
    WorkflowNode, 
    WorkflowEdge,
    NodeType,
    Execution,
    ExecutionStatus,
    ExecutionStep,
)
from agents import BaseAgent, AGENT_REGISTRY, create_agent
from tools import tool_registry


class ToolNode(Node):
    """Node wrapper pour exécuter un outil"""
    
    def __init__(self, tool_name: str, **kwargs):
        super().__init__(**kwargs)
        self.tool_name = tool_name
    
    def prep(self, shared: Dict) -> Dict:
        """Prépare les arguments de l'outil depuis le shared state"""
        return shared.get(f"{self.tool_name}_args", {})
    
    def exec(self, args: Dict) -> Any:
        """Exécute l'outil"""
        return tool_registry.execute(self.tool_name, **args)
    
    def post(self, shared: Dict, prep_res: Any, exec_res: Any) -> str:
        """Stocke le résultat"""
        shared[f"{self.tool_name}_result"] = exec_res
        return "default"


class WorkflowEngine:
    """Moteur d'exécution de workflows basé sur PocketFlow"""
    
    def __init__(self):
        self.agent_registry: Dict[str, Type[BaseAgent]] = AGENT_REGISTRY.copy()
        self.executions: Dict[str, Execution] = {}
    
    def register_agent(self, name: str, agent_class: Type[BaseAgent]):
        """Enregistre un type d'agent"""
        self.agent_registry[name] = agent_class
    
    def build_flow(self, definition: WorkflowDefinition) -> Flow:
        """Construit un Flow PocketFlow à partir d'une définition"""
        
        # 1. Créer les instances de nodes
        nodes: Dict[str, Node] = {}
        
        for node_def in definition.nodes:
            node_id = str(node_def.id)
            
            if node_def.type == NodeType.AGENT:
                agent_type = node_def.agent_type
                if agent_type and agent_type in self.agent_registry:
                    # Créer l'agent avec la config personnalisée
                    config_overrides = node_def.config.get("config_overrides", {})
                    nodes[node_id] = create_agent(
                        agent_type, 
                        config_overrides=config_overrides
                    )
            
            elif node_def.type == NodeType.TOOL:
                if node_def.tool_name:
                    nodes[node_id] = ToolNode(node_def.tool_name)
        
        # 2. Connecter les edges
        for edge in definition.edges:
            source_id = str(edge.source)
            target_id = str(edge.target)
            
            source = nodes.get(source_id)
            target = nodes.get(target_id)
            
            if source and target:
                if edge.condition:
                    # Connexion conditionnelle
                    source - edge.condition >> target
                else:
                    # Connexion par défaut
                    source >> target
        
        # 3. Identifier le node de départ
        start_node = self._find_start_node(definition, nodes)
        
        if not start_node:
            raise ValueError("Aucun node de départ trouvé dans le workflow")
        
        return Flow(start=start_node)
    
    def _find_start_node(
        self, 
        definition: WorkflowDefinition, 
        nodes: Dict[str, Node]
    ) -> Optional[Node]:
        """Trouve le node de départ (sans edge entrant)"""
        
        # Trouver tous les nodes cibles
        target_ids = {str(edge.target) for edge in definition.edges}
        
        # Le node de départ n'est cible d'aucun edge
        for node_def in definition.nodes:
            node_id = str(node_def.id)
            if node_id not in target_ids and node_id in nodes:
                return nodes[node_id]
        
        # Fallback: premier node
        if definition.nodes and str(definition.nodes[0].id) in nodes:
            return nodes[str(definition.nodes[0].id)]
        
        return None
    
    def run(
        self, 
        definition: WorkflowDefinition, 
        input_data: Dict,
        user_id: Optional[UUID] = None
    ) -> Execution:
        """Exécute un workflow de manière synchrone"""
        
        # Créer l'exécution
        execution = Execution(
            workflow_id=definition.id,
            input_data=input_data,
            status=ExecutionStatus.RUNNING,
            user_id=user_id
        )
        self.executions[str(execution.id)] = execution
        
        try:
            # Construire et exécuter le flow
            flow = self.build_flow(definition)
            shared = input_data.copy()
            
            result = flow.run(shared)
            
            # Mettre à jour l'exécution
            execution.status = ExecutionStatus.COMPLETED
            execution.output_data = result
            execution.completed_at = datetime.utcnow()
            
        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.error = str(e)
            execution.completed_at = datetime.utcnow()
        
        return execution
    
    async def run_async(
        self, 
        definition: WorkflowDefinition, 
        input_data: Dict,
        user_id: Optional[UUID] = None
    ) -> Execution:
        """Exécute un workflow de manière asynchrone"""
        
        execution = Execution(
            workflow_id=definition.id,
            input_data=input_data,
            status=ExecutionStatus.RUNNING,
            user_id=user_id
        )
        self.executions[str(execution.id)] = execution
        
        try:
            flow = self.build_flow(definition)
            shared = input_data.copy()
            
            result = await flow.run_async(shared)
            
            execution.status = ExecutionStatus.COMPLETED
            execution.output_data = result
            execution.completed_at = datetime.utcnow()
            
        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.error = str(e)
            execution.completed_at = datetime.utcnow()
        
        return execution
    
    def get_execution(self, execution_id: str) -> Optional[Execution]:
        """Récupère une exécution par son ID"""
        return self.executions.get(execution_id)


# =============================================================================
# TEMPLATES DE WORKFLOWS
# =============================================================================

def create_content_pipeline() -> WorkflowDefinition:
    """Crée un workflow de création de contenu"""
    from uuid import uuid4
    
    # Créer les nodes
    research_node = WorkflowNode(
        id=uuid4(),
        type=NodeType.AGENT,
        agent_type="research",
        position={"x": 100, "y": 100}
    )
    
    writer_node = WorkflowNode(
        id=uuid4(),
        type=NodeType.AGENT,
        agent_type="writer",
        position={"x": 300, "y": 100}
    )
    
    reviewer_node = WorkflowNode(
        id=uuid4(),
        type=NodeType.AGENT,
        agent_type="reviewer",
        position={"x": 500, "y": 100}
    )
    
    # Créer les edges
    edges = [
        # Research -> Write (condition: ready)
        WorkflowEdge(
            source=research_node.id,
            target=writer_node.id,
            condition="write"
        ),
        # Research -> Research (boucle si confidence low)
        WorkflowEdge(
            source=research_node.id,
            target=research_node.id,
            condition="research"
        ),
        # Writer -> Reviewer
        WorkflowEdge(
            source=writer_node.id,
            target=reviewer_node.id,
            condition="review"
        ),
        # Reviewer -> Writer (révision nécessaire)
        WorkflowEdge(
            source=reviewer_node.id,
            target=writer_node.id,
            condition="write"
        ),
    ]
    
    return WorkflowDefinition(
        name="Content Pipeline",
        description="Pipeline de création de contenu: recherche → rédaction → révision",
        nodes=[research_node, writer_node, reviewer_node],
        edges=edges,
        input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Sujet de recherche"},
                "style_guide": {"type": "string", "description": "Guide de style"}
            },
            "required": ["query"]
        }
    )


def create_code_generation_pipeline() -> WorkflowDefinition:
    """Crée un workflow de génération de code"""
    from uuid import uuid4
    
    coder_node = WorkflowNode(
        id=uuid4(),
        type=NodeType.AGENT,
        agent_type="coder",
        position={"x": 100, "y": 100}
    )
    
    reviewer_node = WorkflowNode(
        id=uuid4(),
        type=NodeType.AGENT,
        agent_type="reviewer",
        config={"config_overrides": {
            "system_prompt": """Vous êtes un expert en revue de code.
Vérifiez: syntaxe, bonnes pratiques, sécurité, performance.

Sortie YAML:
```yaml
approved: true/false
issues:
  - issue: <problème>
    severity: high/medium/low
    suggestion: <correction>
```"""
        }},
        position={"x": 300, "y": 100}
    )
    
    edges = [
        WorkflowEdge(
            source=coder_node.id,
            target=reviewer_node.id,
            condition="default"
        ),
        WorkflowEdge(
            source=reviewer_node.id,
            target=coder_node.id,
            condition="write"
        ),
    ]
    
    return WorkflowDefinition(
        name="Code Generation Pipeline",
        description="Pipeline de génération de code avec revue",
        nodes=[coder_node, reviewer_node],
        edges=edges,
        input_schema={
            "type": "object",
            "properties": {
                "coding_task": {"type": "string"},
                "language": {"type": "string", "default": "python"}
            },
            "required": ["coding_task"]
        }
    )


# Templates disponibles
WORKFLOW_TEMPLATES = {
    "content_pipeline": create_content_pipeline,
    "code_generation": create_code_generation_pipeline,
}


def create_workflow_from_template(template_name: str) -> WorkflowDefinition:
    """Crée un workflow à partir d'un template"""
    if template_name not in WORKFLOW_TEMPLATES:
        raise ValueError(f"Template inconnu: {template_name}. "
                        f"Disponibles: {list(WORKFLOW_TEMPLATES.keys())}")
    return WORKFLOW_TEMPLATES[template_name]()


# Instance globale du moteur
workflow_engine = WorkflowEngine()


__all__ = [
    "WorkflowEngine",
    "ToolNode",
    "workflow_engine",
    "create_content_pipeline",
    "create_code_generation_pipeline",
    "create_workflow_from_template",
    "WORKFLOW_TEMPLATES",
]
