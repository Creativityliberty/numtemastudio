"""
Tests pour Nümtema Agents Studio
"""

import pytest
from uuid import uuid4

# =============================================================================
# TESTS POCKETFLOW
# =============================================================================

def test_node_basic():
    """Test du Node de base"""
    from pocketflow import Node
    
    class TestNode(Node):
        def exec(self, prep_res):
            return f"processed: {prep_res}"
    
    node = TestNode()
    shared = {"input": "test"}
    
    # Test prep par défaut
    assert node.prep(shared) is None
    
    # Test exec
    assert node.exec("hello") == "processed: hello"
    
    # Test post par défaut
    assert node.post(shared, None, None) == "default"


def test_node_connections():
    """Test des connexions entre nodes"""
    from pocketflow import Node
    
    class NodeA(Node):
        def exec(self, prep_res):
            return "A"
    
    class NodeB(Node):
        def exec(self, prep_res):
            return "B"
    
    a = NodeA()
    b = NodeB()
    
    # Test connexion simple
    a >> b
    assert a.successors.get("default") == b


def test_conditional_connections():
    """Test des connexions conditionnelles"""
    from pocketflow import Node
    
    class RouterNode(Node):
        def exec(self, prep_res):
            return prep_res
        
        def post(self, shared, prep_res, exec_res):
            return "yes" if exec_res else "no"
    
    class YesNode(Node):
        def exec(self, prep_res):
            return "YES"
    
    class NoNode(Node):
        def exec(self, prep_res):
            return "NO"
    
    router = RouterNode()
    yes = YesNode()
    no = NoNode()
    
    router - "yes" >> yes
    router - "no" >> no
    
    assert router.successors.get("yes") == yes
    assert router.successors.get("no") == no


def test_flow_execution():
    """Test de l'exécution d'un flow"""
    from pocketflow import Node, Flow
    
    class AddNode(Node):
        def prep(self, shared):
            return shared.get("value", 0)
        
        def exec(self, value):
            return value + 1
        
        def post(self, shared, prep_res, exec_res):
            shared["value"] = exec_res
            return "default"
    
    node1 = AddNode()
    node2 = AddNode()
    node3 = AddNode()
    
    node1 >> node2 >> node3
    
    flow = Flow(start=node1)
    result = flow.run({"value": 0})
    
    assert result["value"] == 3


# =============================================================================
# TESTS MODELS
# =============================================================================

def test_agent_config():
    """Test de la configuration d'agent"""
    from models import AgentConfig, LLMProvider
    
    config = AgentConfig(
        name="Test Agent",
        system_prompt="You are a test agent",
        model_provider=LLMProvider.OPENAI,
        model_name="gpt-4o"
    )
    
    assert config.name == "Test Agent"
    assert config.model_provider == LLMProvider.OPENAI
    assert config.max_retries == 3  # default


def test_workflow_definition():
    """Test de la définition de workflow"""
    from models import WorkflowDefinition, WorkflowNode, WorkflowEdge, NodeType
    
    node1 = WorkflowNode(
        type=NodeType.AGENT,
        agent_type="research"
    )
    
    node2 = WorkflowNode(
        type=NodeType.AGENT,
        agent_type="writer"
    )
    
    edge = WorkflowEdge(
        source=node1.id,
        target=node2.id
    )
    
    workflow = WorkflowDefinition(
        name="Test Workflow",
        nodes=[node1, node2],
        edges=[edge]
    )
    
    assert workflow.name == "Test Workflow"
    assert len(workflow.nodes) == 2
    assert len(workflow.edges) == 1


# =============================================================================
# TESTS TOOLS
# =============================================================================

def test_calculator_tool():
    """Test de l'outil calculatrice"""
    from tools import calculator
    
    result = calculator("2 + 2")
    assert result["success"] is True
    assert result["result"] == 4
    
    result = calculator("10 * 5")
    assert result["success"] is True
    assert result["result"] == 50


def test_calculator_tool_error():
    """Test de l'outil calculatrice avec erreur"""
    from tools import calculator
    
    # Expression invalide
    result = calculator("invalid")
    assert result["success"] is False
    assert "error" in result


def test_tool_registry():
    """Test du registre d'outils"""
    from tools import tool_registry
    
    # Vérifier que les outils standards sont enregistrés
    tools = tool_registry.list_tools()
    tool_names = [t["name"] for t in tools]
    
    assert "calculator" in tool_names
    assert "web_search" in tool_names


# =============================================================================
# TESTS WORKFLOWS
# =============================================================================

def test_content_pipeline_template():
    """Test du template de pipeline de contenu"""
    from workflows import create_content_pipeline
    
    workflow = create_content_pipeline()
    
    assert workflow.name == "Content Pipeline"
    assert len(workflow.nodes) == 3  # research, writer, reviewer
    assert len(workflow.edges) == 4


def test_workflow_engine():
    """Test du moteur de workflow"""
    from workflows import WorkflowEngine
    from models import WorkflowDefinition, WorkflowNode, WorkflowEdge, NodeType
    
    engine = WorkflowEngine()
    
    # Vérifier que les types d'agents sont enregistrés
    assert "research" in engine.agent_registry
    assert "writer" in engine.agent_registry
    assert "reviewer" in engine.agent_registry


# =============================================================================
# TESTS API
# =============================================================================

@pytest.mark.asyncio
async def test_api_health():
    """Test du endpoint health"""
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_api_list_agent_types():
    """Test de la liste des types d'agents"""
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    response = client.get("/api/v1/agents/types")
    
    assert response.status_code == 200
    data = response.json()
    assert "research" in data["types"]
    assert "writer" in data["types"]


@pytest.mark.asyncio
async def test_api_list_workflow_templates():
    """Test de la liste des templates de workflows"""
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    response = client.get("/api/v1/workflows/templates")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["templates"]) > 0


@pytest.mark.asyncio
async def test_api_list_tools():
    """Test de la liste des outils"""
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    response = client.get("/api/v1/tools")
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0


@pytest.mark.asyncio
async def test_api_execute_tool():
    """Test de l'exécution d'un outil via API"""
    from fastapi.testclient import TestClient
    from api.main import app
    
    client = TestClient(app)
    response = client.post(
        "/api/v1/tools/calculator/execute",
        json={"expression": "3 + 4"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["result"]["result"] == 7


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
