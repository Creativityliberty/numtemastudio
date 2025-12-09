"""
Exemples d'utilisation des Builder Tools (MCP Protocol)

Les builder_tools sont des outils MCP qui permettent au Agent Builder
de créer, modifier, supprimer et lister les agents et workflows.
"""

import json
from tools import tool_registry
from tools.builder_tools import (
    create_agent,
    update_agent,
    delete_agent,
    list_agents,
    get_agent,
    create_workflow,
    update_workflow,
    delete_workflow,
    list_workflows,
    get_workflow
)


def print_result(title: str, result: dict):
    """Affiche un résultat formaté"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


# =============================================================================
# AGENT TOOLS EXAMPLES
# =============================================================================

def example_create_agent():
    """Exemple: Créer un agent"""
    print_result(
        "EXEMPLE 1: Créer un agent",
        create_agent(
            name="TranslatorAgent",
            description="Agent spécialisé en traduction",
            agent_type="custom",
            config={
                "model_name": "gpt-4o",
                "temperature": 0.7,
                "max_retries": 3
            },
            tags=["translation", "nlp"]
        )
    )


def example_list_agents():
    """Exemple: Lister les agents"""
    # Créer quelques agents d'abord
    create_agent("ResearchAgent", agent_type="research", tags=["research"])
    create_agent("WriterAgent", agent_type="writer", tags=["writing"])
    create_agent("TranslatorAgent", agent_type="custom", tags=["translation"])
    
    print_result(
        "EXEMPLE 2: Lister tous les agents",
        list_agents()
    )
    
    print_result(
        "EXEMPLE 2b: Lister les agents avec tag 'translation'",
        list_agents(tag="translation")
    )


def example_get_agent():
    """Exemple: Récupérer un agent"""
    # Créer un agent d'abord
    result = create_agent("SummarizerAgent", description="Résume du texte")
    agent_id = result["agent"]["id"]
    
    print_result(
        "EXEMPLE 3: Récupérer un agent",
        get_agent(agent_id)
    )


def example_update_agent():
    """Exemple: Mettre à jour un agent"""
    # Créer un agent d'abord
    result = create_agent("EditorAgent", description="Édite du contenu")
    agent_id = result["agent"]["id"]
    
    print_result(
        "EXEMPLE 4: Mettre à jour un agent",
        update_agent(
            agent_id=agent_id,
            description="Édite et améliore du contenu",
            config={"temperature": 0.8}
        )
    )


def example_delete_agent():
    """Exemple: Supprimer un agent"""
    # Créer un agent d'abord
    result = create_agent("TemporaryAgent", description="Agent temporaire")
    agent_id = result["agent"]["id"]
    
    print_result(
        "EXEMPLE 5: Supprimer un agent",
        delete_agent(agent_id)
    )


# =============================================================================
# WORKFLOW TOOLS EXAMPLES
# =============================================================================

def example_create_workflow():
    """Exemple: Créer un workflow"""
    print_result(
        "EXEMPLE 6: Créer un workflow",
        create_workflow(
            name="ContentPipeline",
            description="Pipeline complet de création de contenu",
            nodes=[
                {"id": "research", "type": "ResearchAgent", "label": "Recherche"},
                {"id": "write", "type": "WriterAgent", "label": "Rédaction"},
                {"id": "review", "type": "ReviewerAgent", "label": "Révision"}
            ],
            edges=[
                {"from": "research", "to": "write", "label": "write"},
                {"from": "write", "to": "review", "label": "review"}
            ]
        )
    )


def example_list_workflows():
    """Exemple: Lister les workflows"""
    # Créer quelques workflows d'abord
    create_workflow("Pipeline1", nodes=[], edges=[])
    create_workflow("Pipeline2", nodes=[], edges=[])
    
    print_result(
        "EXEMPLE 7: Lister tous les workflows",
        list_workflows()
    )


def example_get_workflow():
    """Exemple: Récupérer un workflow"""
    # Créer un workflow d'abord
    result = create_workflow("MyWorkflow", description="Mon workflow")
    workflow_id = result["workflow"]["id"]
    
    print_result(
        "EXEMPLE 8: Récupérer un workflow",
        get_workflow(workflow_id)
    )


def example_update_workflow():
    """Exemple: Mettre à jour un workflow"""
    # Créer un workflow d'abord
    result = create_workflow("UpdateableWorkflow", nodes=[], edges=[])
    workflow_id = result["workflow"]["id"]
    
    print_result(
        "EXEMPLE 9: Mettre à jour un workflow",
        update_workflow(
            workflow_id=workflow_id,
            description="Workflow mis à jour",
            nodes=[
                {"id": "step1", "type": "Agent1"},
                {"id": "step2", "type": "Agent2"}
            ],
            edges=[
                {"from": "step1", "to": "step2"}
            ]
        )
    )


def example_delete_workflow():
    """Exemple: Supprimer un workflow"""
    # Créer un workflow d'abord
    result = create_workflow("DeleteableWorkflow")
    workflow_id = result["workflow"]["id"]
    
    print_result(
        "EXEMPLE 10: Supprimer un workflow",
        delete_workflow(workflow_id)
    )


# =============================================================================
# TOOL REGISTRY EXAMPLES
# =============================================================================

def example_tool_registry():
    """Exemple: Utiliser les tools via le registre"""
    print("\n" + "="*60)
    print("  EXEMPLE 11: Utiliser les tools via le registre")
    print("="*60)
    
    # Lister les tools disponibles
    builder_tools = tool_registry.list_tools(category="builder")
    print(f"\n✅ {len(builder_tools)} builder tools disponibles:")
    for tool in builder_tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # Exécuter un tool via le registre
    print("\n📋 Exécution de 'create_agent' via le registre:")
    result = tool_registry.execute(
        "create_agent",
        name="RegistryAgent",
        description="Agent créé via le registre",
        agent_type="custom"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


# =============================================================================
# AGENT BUILDER WITH TOOLS EXAMPLE
# =============================================================================

def example_agent_builder_with_tools():
    """Exemple: Agent Builder utilisant les tools MCP"""
    from agents import AgentBuilder
    
    print("\n" + "="*60)
    print("  EXEMPLE 12: Agent Builder avec MCP Tools")
    print("="*60)
    
    # Créer le builder
    builder = AgentBuilder()
    builder.register_tool_registry(tool_registry)
    
    # Préparer le contexte
    shared = {
        "builder_request": "Crée un nouvel agent appelé AnalyzerAgent",
        "agents_list": [],
        "workflows_list": [],
        "builder_context": {}
    }
    
    # Exécuter le builder
    action = builder.run(shared)
    
    print(f"\n✅ Action exécutée: {shared.get('last_action')}")
    print(f"📊 Résultat:")
    print(json.dumps(shared.get("builder_result"), indent=2, ensure_ascii=False))


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n🛠️  BUILDER TOOLS - EXEMPLES D'UTILISATION\n")
    
    # Exemples des tools individuels
    example_create_agent()
    example_list_agents()
    example_get_agent()
    example_update_agent()
    example_delete_agent()
    
    example_create_workflow()
    example_list_workflows()
    example_get_workflow()
    example_update_workflow()
    example_delete_workflow()
    
    # Exemples du registre
    example_tool_registry()
    
    # Exemple du builder avec tools
    example_agent_builder_with_tools()
    
    print("\n✅ Tous les exemples sont terminés!\n")
