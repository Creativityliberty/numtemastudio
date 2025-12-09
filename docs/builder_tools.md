# Builder Tools - Documentation MCP

## 🎯 Vue d'ensemble

Les **Builder Tools** sont des outils MCP (Model Context Protocol) qui permettent à l'Agent Builder d'exécuter des opérations CRUD sur les agents et workflows de manière sécurisée et standardisée.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Builder                            │
│                                                              │
│  LLM décide: "Je dois créer un agent"                      │
│                    │                                        │
│                    ▼                                        │
│  Retourne JSON:                                            │
│  {                                                          │
│    "tool": "create_agent",                                 │
│    "parameters": {                                          │
│      "name": "TranslatorAgent",                            │
│      "description": "..."                                  │
│    }                                                        │
│  }                                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Tool Registry (MCP)                            │
│                                                              │
│  tool_registry.execute("create_agent", **params)           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Builder Tools                                  │
│                                                              │
│  create_agent(name, description, config, ...)              │
│    └─ Crée l'agent                                         │
│    └─ Retourne le résultat                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Storage                                        │
│                                                              │
│  agents_storage[agent_id] = agent                          │
│  workflows_storage[workflow_id] = workflow                 │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Tools Disponibles

### Agent Tools

#### 1. `create_agent`

Crée un nouvel agent.

**Paramètres:**
```python
create_agent(
    name: str,                          # Nom de l'agent (requis)
    description: str = "",              # Description
    agent_type: str = "custom",         # Type: research, writer, reviewer, coder, custom
    config: Dict[str, Any] = None,      # Configuration (model_name, temperature, etc.)
    tags: List[str] = None              # Tags pour catégoriser
)
```

**Réponse:**
```json
{
  "success": true,
  "status": "created",
  "agent": {
    "id": "agent_translatoragent_a1b2c3d4",
    "name": "TranslatorAgent",
    "description": "Agent spécialisé en traduction",
    "type": "custom",
    "config": {...},
    "tags": ["translation"],
    "created_at": "2025-12-09T16:45:00",
    "updated_at": "2025-12-09T16:45:00",
    "status": "active"
  },
  "message": "Agent 'TranslatorAgent' créé avec succès"
}
```

#### 2. `update_agent`

Met à jour un agent existant.

**Paramètres:**
```python
update_agent(
    agent_id: str,                      # ID de l'agent (requis)
    name: str = None,                   # Nouveau nom
    description: str = None,            # Nouvelle description
    config: Dict[str, Any] = None,      # Nouvelle configuration
    tags: List[str] = None              # Nouveaux tags
)
```

**Réponse:**
```json
{
  "success": true,
  "status": "updated",
  "agent": {...},
  "message": "Agent 'agent_id' mis à jour avec succès"
}
```

#### 3. `delete_agent`

Supprime un agent.

**Paramètres:**
```python
delete_agent(
    agent_id: str                       # ID de l'agent (requis)
)
```

**Réponse:**
```json
{
  "success": true,
  "status": "deleted",
  "agent_id": "agent_translatoragent_a1b2c3d4",
  "agent_name": "TranslatorAgent",
  "message": "Agent 'TranslatorAgent' supprimé avec succès"
}
```

#### 4. `list_agents`

Liste les agents disponibles.

**Paramètres:**
```python
list_agents(
    agent_type: str = None,             # Filtrer par type
    tag: str = None,                    # Filtrer par tag
    limit: int = 100,                   # Nombre max d'agents
    offset: int = 0                     # Décalage pour pagination
)
```

**Réponse:**
```json
{
  "success": true,
  "status": "listed",
  "agents": [...],
  "total": 5,
  "count": 5,
  "offset": 0,
  "limit": 100,
  "message": "5 agent(s) trouvé(s)"
}
```

#### 5. `get_agent`

Récupère les détails d'un agent.

**Paramètres:**
```python
get_agent(
    agent_id: str                       # ID de l'agent (requis)
)
```

**Réponse:**
```json
{
  "success": true,
  "status": "retrieved",
  "agent": {...},
  "message": "Agent 'TranslatorAgent' récupéré avec succès"
}
```

### Workflow Tools

#### 6. `create_workflow`

Crée un nouveau workflow.

**Paramètres:**
```python
create_workflow(
    name: str,                          # Nom du workflow (requis)
    description: str = "",              # Description
    nodes: List[Dict] = None,           # Nœuds du workflow
    edges: List[Dict] = None,           # Connexions entre nœuds
    input_schema: Dict = None,          # Schéma d'entrée
    output_schema: Dict = None          # Schéma de sortie
)
```

**Réponse:**
```json
{
  "success": true,
  "status": "created",
  "workflow": {
    "id": "workflow_contentpipeline_a1b2c3d4",
    "name": "ContentPipeline",
    "description": "Pipeline complet de création de contenu",
    "nodes": [...],
    "edges": [...],
    "created_at": "2025-12-09T16:45:00",
    "updated_at": "2025-12-09T16:45:00",
    "status": "active",
    "version": 1
  },
  "message": "Workflow 'ContentPipeline' créé avec succès"
}
```

#### 7. `update_workflow`

Met à jour un workflow existant.

**Paramètres:**
```python
update_workflow(
    workflow_id: str,                   # ID du workflow (requis)
    name: str = None,                   # Nouveau nom
    description: str = None,            # Nouvelle description
    nodes: List[Dict] = None,           # Nouveaux nœuds
    edges: List[Dict] = None,           # Nouvelles connexions
    input_schema: Dict = None,          # Nouveau schéma d'entrée
    output_schema: Dict = None          # Nouveau schéma de sortie
)
```

#### 8. `delete_workflow`

Supprime un workflow.

**Paramètres:**
```python
delete_workflow(
    workflow_id: str                    # ID du workflow (requis)
)
```

#### 9. `list_workflows`

Liste les workflows disponibles.

**Paramètres:**
```python
list_workflows(
    limit: int = 100,                   # Nombre max de workflows
    offset: int = 0                     # Décalage pour pagination
)
```

#### 10. `get_workflow`

Récupère les détails d'un workflow.

**Paramètres:**
```python
get_workflow(
    workflow_id: str                    # ID du workflow (requis)
)
```

## 🔌 Utilisation via le Registre

### Exécuter un tool directement

```python
from tools import tool_registry

# Créer un agent
result = tool_registry.execute(
    "create_agent",
    name="TranslatorAgent",
    description="Agent de traduction",
    agent_type="custom"
)

print(result)
```

### Lister les tools disponibles

```python
# Lister tous les builder tools
builder_tools = tool_registry.list_tools(category="builder")

for tool in builder_tools:
    print(f"{tool['name']}: {tool['description']}")
```

## 🤖 Utilisation avec Agent Builder

### Exemple 1: Créer un agent via le builder

```python
from agents import AgentBuilder
from tools import tool_registry

# Créer le builder
builder = AgentBuilder()
builder.register_tool_registry(tool_registry)

# Préparer le contexte
shared = {
    "builder_request": "Crée un nouvel agent TranslatorAgent",
    "agents_list": [],
    "workflows_list": [],
    "builder_context": {}
}

# Exécuter
action = builder.run(shared)

# Résultat
print(shared["builder_result"])
```

### Exemple 2: Créer un workflow via le builder

```python
shared = {
    "builder_request": "Crée un workflow qui enchaîne ResearchAgent -> WriterAgent",
    "agents_list": [],
    "workflows_list": [],
    "builder_context": {}
}

action = builder.run(shared)
print(shared["builder_result"])
```

## 🔄 Flux Complet

```
1. Utilisateur envoie requête
   "Crée un agent TranslatorAgent"
        │
        ▼
2. AgentBuilder.prep()
   Extrait la requête
        │
        ▼
3. AgentBuilder.exec()
   Appel LLM
   LLM retourne:
   {
     "tool": "create_agent",
     "parameters": {
       "name": "TranslatorAgent",
       "description": "..."
     }
   }
        │
        ▼
4. AgentBuilder.post()
   tool_registry.execute("create_agent", **params)
        │
        ▼
5. create_agent()
   Crée l'agent
   Stocke dans agents_storage
   Retourne le résultat
        │
        ▼
6. Résultat retourné à l'utilisateur
   {
     "success": true,
     "status": "created",
     "agent": {...}
   }
```

## 📊 Format des Réponses

Tous les tools retournent un dictionnaire avec:

```python
{
    "success": bool,           # Succès de l'opération
    "status": str,             # Status: created, updated, deleted, listed, retrieved
    "message": str,            # Message descriptif
    "agent": dict,             # (optionnel) Agent créé/modifié
    "agents": list,            # (optionnel) Liste d'agents
    "workflow": dict,          # (optionnel) Workflow créé/modifié
    "workflows": list,         # (optionnel) Liste de workflows
    "error": str,              # (optionnel) Message d'erreur
    "total": int,              # (optionnel) Nombre total
    "count": int               # (optionnel) Nombre retourné
}
```

## 🔐 Sécurité

- ✅ Validation des paramètres
- ✅ Gestion des erreurs
- ✅ Pas d'exécution de code arbitraire
- ✅ IDs générés automatiquement
- ✅ Timestamps automatiques

## 📈 Stockage

Les tools utilisent actuellement un stockage en mémoire:

```python
agents_storage: Dict[str, Dict] = {}
workflows_storage: Dict[str, Dict] = {}
```

**Pour la production**, remplacer par:
- PostgreSQL avec SQLAlchemy
- Redis pour le cache
- Qdrant pour les embeddings

## 🚀 Intégration API

Les builder_tools sont automatiquement disponibles via:

```bash
POST /api/v1/builder/execute
{
  "request": "Crée un nouvel agent TranslatorAgent",
  "context": {}
}
```

## 📚 Ressources

- [Exemples d'utilisation](../examples/builder_tools_example.py)
- [Agent Builder Documentation](./agent_builder.md)
- [Architecture Complète](./architecture_with_builder.md)
