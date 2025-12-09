# Agent Builder - Documentation

## 🎯 Vue d'ensemble

L'**Agent Builder** est un agent spécialisé qui gère la création, modification, suppression et listage des agents et workflows. Il agit comme un orchestrateur central capable de comprendre des requêtes en langage naturel et de les traduire en actions CRUD.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      UTILISATEUR / API                          │
│                                                                  │
│  "Crée un nouvel agent appelé TranslatorAgent"                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT BUILDER                                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ prep()                                                   │  │
│  │ - Extrait la requête utilisateur                        │  │
│  │ - Récupère la liste des agents/workflows               │  │
│  │ - Prépare le contexte                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ exec() - Appel LLM                                       │  │
│  │ - Envoie la requête au LLM                              │  │
│  │ - LLM décide de l'action (create/update/delete/list)   │  │
│  │ - Retourne JSON structuré                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ post() - Exécution                                       │  │
│  │ - Parse la réponse JSON                                 │  │
│  │ - Exécute l'action correspondante                       │  │
│  │ - Retourne le résultat                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RÉSULTAT                                     │
│                                                                  │
│  {                                                              │
│    "status": "created",                                         │
│    "type": "agent",                                             │
│    "name": "TranslatorAgent",                                   │
│    "id": "agent_translatoragent"                                │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Actions Disponibles

### Agents

| Action | Description | Paramètres |
|--------|-------------|-----------|
| `create_agent` | Crée un nouvel agent | `name`, `description`, `config` |
| `update_agent` | Met à jour un agent | `id`, `config` |
| `delete_agent` | Supprime un agent | `id` |
| `list_agents` | Liste tous les agents | - |
| `get_agent` | Récupère les détails d'un agent | `id` |

### Workflows

| Action | Description | Paramètres |
|--------|-------------|-----------|
| `create_workflow` | Crée un nouveau workflow | `name`, `description`, `nodes`, `edges` |
| `update_workflow` | Met à jour un workflow | `id`, `nodes`, `edges` |
| `delete_workflow` | Supprime un workflow | `id` |
| `list_workflows` | Liste tous les workflows | - |
| `get_workflow` | Récupère les détails d'un workflow | `id` |

## 🔌 Intégration API

### Endpoint 1: Exécuter le Builder

```bash
POST /api/v1/builder/execute
Content-Type: application/json

{
  "request": "Crée un nouvel agent appelé TranslatorAgent",
  "context": {
    "language": "français",
    "domain": "traduction"
  }
}
```

**Réponse:**
```json
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
```

### Endpoint 2: Récupérer les Capacités

```bash
GET /api/v1/builder/capabilities
```

**Réponse:**
```json
{
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
```

## 💻 Utilisation Programmatique

### Exemple 1: Créer un agent

```python
from agents import AgentBuilder

builder = AgentBuilder()

shared = {
    "builder_request": "Crée un nouvel agent appelé TranslatorAgent",
    "agents_list": [],
    "workflows_list": [],
    "builder_context": {}
}

action = builder.run(shared)
print(shared["builder_result"])
```

### Exemple 2: Utiliser dans un Flow

```python
from agents import AgentBuilder
from pocketflow import Flow

builder = AgentBuilder()
flow = Flow(start=builder)

shared = {
    "builder_request": "Liste tous les agents",
    "agents_list": [],
    "workflows_list": [],
    "builder_context": {}
}

result = flow.run(shared)
print(result["builder_result"])
```

### Exemple 3: Créer un workflow avec le builder

```python
shared = {
    "builder_request": "Crée un workflow qui enchaîne ResearchAgent -> WriterAgent",
    "agents_list": [
        {"name": "ResearchAgent", "id": "research_1"},
        {"name": "WriterAgent", "id": "writer_1"}
    ],
    "workflows_list": [],
    "builder_context": {
        "workflow_name": "ContentPipeline"
    }
}

action = builder.run(shared)
print(shared["builder_result"])
```

## 🔄 Flux de Traitement

```
Requête Utilisateur
        │
        ▼
    prep()
    ├─ Extrait la requête
    ├─ Récupère les agents/workflows
    └─ Prépare le contexte
        │
        ▼
    exec() - Appel LLM
    ├─ Envoie au LLM
    ├─ LLM analyse la requête
    └─ Retourne JSON structuré
        │
        ▼
    post() - Exécution
    ├─ Parse la réponse
    ├─ Valide l'action
    ├─ Exécute l'action
    └─ Retourne le résultat
        │
        ▼
    Résultat
```

## 🎨 Format de Sortie du LLM

Le LLM doit retourner un JSON structuré:

```json
{
  "action": "create_agent|update_agent|delete_agent|list_agents|get_agent|create_workflow|update_workflow|delete_workflow|list_workflows|get_workflow",
  "parameters": {
    "id": "optional - ID de l'agent/workflow",
    "name": "optional - nom",
    "description": "optional - description",
    "config": "optional - configuration",
    "nodes": "optional - nœuds du workflow",
    "edges": "optional - connexions du workflow"
  },
  "reason": "Explication de l'action"
}
```

## 🚀 Cas d'Usage

### 1. Interface de Gestion Centralisée

L'Agent Builder permet une interface unique pour gérer tous les agents et workflows via langage naturel.

```
Utilisateur: "Crée un agent de traduction et ajoute-le au workflow ContentPipeline"
Builder: Crée l'agent + met à jour le workflow
```

### 2. Automatisation de Configuration

Automatiser la création et la configuration d'agents basée sur des templates.

```
Utilisateur: "Crée 3 agents: Translator, Summarizer, Editor"
Builder: Crée les 3 agents en parallèle
```

### 3. Gestion Dynamique

Modifier les agents et workflows en fonction des besoins en temps réel.

```
Utilisateur: "Augmente la température du WriterAgent à 0.9"
Builder: Met à jour la configuration
```

## ⚙️ Configuration

L'Agent Builder utilise les mêmes paramètres que les autres agents:

```python
AgentBuilder(
    config_overrides={
        "model_name": "gpt-4o",
        "temperature": 0.7,
        "max_retries": 3
    }
)
```

## 🔐 Sécurité

- Les actions sont validées avant exécution
- Les paramètres sont vérifiés
- Les erreurs sont capturées et rapportées
- Pas d'exécution de code arbitraire

## 📊 Monitoring

Chaque action du builder génère:
- `last_action`: L'action exécutée
- `builder_result`: Le résultat de l'action
- `builder_error`: Les erreurs (si présentes)

## 🔗 Intégration avec d'autres Agents

L'Agent Builder peut être utilisé dans des pipelines complexes:

```
User Input
    │
    ▼
[Agent Builder] ──→ Crée/Modifie agents
    │
    ▼
[Workflow Engine] ──→ Exécute le workflow
    │
    ▼
[Résultat Final]
```

## 📚 Ressources

- [Exemples d'utilisation](../examples/agent_builder_example.py)
- [API Reference](./api.md)
- [Architecture Complète](./architecture.md)
