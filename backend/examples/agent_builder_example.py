"""
Exemple d'utilisation de l'Agent Builder

L'Agent Builder est un agent spécialisé qui peut créer, modifier, lister et supprimer
des agents et workflows via des requêtes en langage naturel.
"""

import asyncio
import json
from agents import AgentBuilder
from pocketflow import Flow


async def example_builder_crud():
    """Exemple: Utiliser l'Agent Builder pour faire des CRUD"""
    
    # Créer une instance du builder
    builder = AgentBuilder()
    
    # Exemple 1: Créer un nouvel agent
    print("=" * 60)
    print("EXEMPLE 1: Créer un nouvel agent")
    print("=" * 60)
    
    shared = {
        "builder_request": "Crée un nouvel agent appelé 'TranslatorAgent' qui traduit du texte",
        "agents_list": [],
        "workflows_list": [],
        "builder_context": {
            "language": "français",
            "domain": "traduction"
        }
    }
    
    action = builder.run(shared)
    print(f"Action: {shared.get('last_action')}")
    print(f"Résultat: {json.dumps(shared.get('builder_result'), indent=2)}")
    print()
    
    # Exemple 2: Lister les agents
    print("=" * 60)
    print("EXEMPLE 2: Lister les agents")
    print("=" * 60)
    
    shared = {
        "builder_request": "Liste tous les agents disponibles",
        "agents_list": [
            {"name": "ResearchAgent", "id": "research_1"},
            {"name": "WriterAgent", "id": "writer_1"},
            {"name": "TranslatorAgent", "id": "translator_1"}
        ],
        "workflows_list": [],
        "builder_context": {}
    }
    
    action = builder.run(shared)
    print(f"Action: {shared.get('last_action')}")
    print(f"Résultat: {json.dumps(shared.get('builder_result'), indent=2)}")
    print()
    
    # Exemple 3: Créer un workflow
    print("=" * 60)
    print("EXEMPLE 3: Créer un workflow")
    print("=" * 60)
    
    shared = {
        "builder_request": "Crée un workflow qui enchaîne ResearchAgent -> WriterAgent -> ReviewerAgent",
        "agents_list": [
            {"name": "ResearchAgent", "id": "research_1"},
            {"name": "WriterAgent", "id": "writer_1"},
            {"name": "ReviewerAgent", "id": "reviewer_1"}
        ],
        "workflows_list": [],
        "builder_context": {
            "workflow_name": "ContentPipeline",
            "description": "Pipeline complet de création de contenu"
        }
    }
    
    action = builder.run(shared)
    print(f"Action: {shared.get('last_action')}")
    print(f"Résultat: {json.dumps(shared.get('builder_result'), indent=2)}")
    print()
    
    # Exemple 4: Mettre à jour un agent
    print("=" * 60)
    print("EXEMPLE 4: Mettre à jour un agent")
    print("=" * 60)
    
    shared = {
        "builder_request": "Mets à jour l'agent 'WriterAgent' pour augmenter sa température à 0.8",
        "agents_list": [
            {"name": "WriterAgent", "id": "writer_1", "temperature": 0.7}
        ],
        "workflows_list": [],
        "builder_context": {
            "agent_id": "writer_1",
            "new_temperature": 0.8
        }
    }
    
    action = builder.run(shared)
    print(f"Action: {shared.get('last_action')}")
    print(f"Résultat: {json.dumps(shared.get('builder_result'), indent=2)}")
    print()
    
    # Exemple 5: Supprimer un agent
    print("=" * 60)
    print("EXEMPLE 5: Supprimer un agent")
    print("=" * 60)
    
    shared = {
        "builder_request": "Supprime l'agent 'TranslatorAgent'",
        "agents_list": [
            {"name": "TranslatorAgent", "id": "translator_1"}
        ],
        "workflows_list": [],
        "builder_context": {
            "agent_id": "translator_1"
        }
    }
    
    action = builder.run(shared)
    print(f"Action: {shared.get('last_action')}")
    print(f"Résultat: {json.dumps(shared.get('builder_result'), indent=2)}")
    print()


async def example_builder_in_flow():
    """Exemple: Utiliser l'Agent Builder dans un Flow"""
    
    print("=" * 60)
    print("EXEMPLE: Agent Builder dans un Flow")
    print("=" * 60)
    
    # Créer le builder
    builder = AgentBuilder()
    
    # Créer un flow avec le builder
    flow = Flow(start=builder)
    
    # Exécuter le flow
    shared = {
        "builder_request": "Crée un nouvel agent appelé 'SummarizerAgent'",
        "agents_list": [],
        "workflows_list": [],
        "builder_context": {}
    }
    
    result = flow.run(shared)
    
    print(f"Résultat du flow: {json.dumps(result.get('builder_result'), indent=2)}")
    print()


async def example_api_usage():
    """Exemple: Utiliser l'Agent Builder via l'API REST"""
    
    print("=" * 60)
    print("EXEMPLE: Utiliser l'Agent Builder via l'API")
    print("=" * 60)
    
    print("""
    # 1. Récupérer les capacités du builder
    curl -X GET http://localhost:8000/api/v1/builder/capabilities
    
    # 2. Exécuter une requête du builder
    curl -X POST http://localhost:8000/api/v1/builder/execute \\
      -H "Content-Type: application/json" \\
      -d '{
        "request": "Crée un nouvel agent appelé TranslatorAgent",
        "context": {
          "language": "français"
        }
      }'
    
    # 3. Exemple de réponse
    {
      "status": "executed",
      "action": "create_agent",
      "result": {
        "status": "created",
        "type": "agent",
        "name": "TranslatorAgent",
        "id": "agent_translatoragent"
      },
      "error": null
    }
    """)


if __name__ == "__main__":
    print("\n🤖 AGENT BUILDER - EXEMPLES D'UTILISATION\n")
    
    # Exécuter les exemples
    asyncio.run(example_builder_crud())
    asyncio.run(example_builder_in_flow())
    asyncio.run(example_api_usage())
    
    print("\n✅ Tous les exemples sont terminés!\n")
