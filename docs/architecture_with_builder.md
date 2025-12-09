# Architecture Complète avec Agent Builder

## 🏗️ Vue d'ensemble Globale

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         UTILISATEUR / FRONTEND                           │
│                                                                           │
│  Interface Web / API Client / CLI                                        │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐        ┌──────────┐      ┌──────────┐
   │ Agents  │        │Workflows │      │  Builder │
   │ Mgmt    │        │  Mgmt    │      │  Mgmt    │
   └────┬────┘        └────┬─────┘      └────┬─────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
┌──────────────────────────────┐    ┌─────────────────────────┐
│   FASTAPI REST API           │    │  AGENT BUILDER          │
│                              │    │                         │
│ POST /api/v1/agents          │    │ ┌───────────────────┐  │
│ GET  /api/v1/agents          │    │ │ prep()            │  │
│ PUT  /api/v1/agents/{id}     │    │ │ - Extract request │  │
│ DELETE /api/v1/agents/{id}   │    │ │ - Get context     │  │
│                              │    │ └───────────────────┘  │
│ POST /api/v1/workflows       │    │         │               │
│ GET  /api/v1/workflows       │    │         ▼               │
│ DELETE /api/v1/workflows/{id}│    │ ┌───────────────────┐  │
│                              │    │ │ exec()            │  │
│ POST /api/v1/builder/execute │    │ │ - Call LLM        │  │
│ GET  /api/v1/builder/capab...│    │ │ - Parse response  │  │
│                              │    │ └───────────────────┘  │
│ POST /api/v1/workflows/{id}  │    │         │               │
│      /execute                │    │         ▼               │
│ GET  /api/v1/executions      │    │ ┌───────────────────┐  │
│                              │    │ │ post()            │  │
│ GET  /api/v1/tools           │    │ │ - Execute action  │  │
│ POST /api/v1/tools/{name}    │    │ │ - Return result   │  │
│      /execute                │    │ └───────────────────┘  │
└──────────────────────────────┘    └─────────────────────────┘
        │                                     │
        └─────────────────┬───────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌──────────────────────────────┐  ┌──────────────────────────┐
│   POCKETFLOW CORE            │  │  AGENT REGISTRY          │
│                              │  │                          │
│ ┌──────────────────────────┐ │  │ - ResearchAgent          │
│ │ Node                     │ │  │ - WriterAgent            │
│ │ ├─ prep()               │ │  │ - ReviewerAgent          │
│ │ ├─ exec()               │ │  │ - CoderAgent             │
│ │ └─ post()               │ │  │ - AgentBuilder           │
│ └──────────────────────────┘ │  │ - Custom Agents          │
│                              │  │                          │
│ ┌──────────────────────────┐ │  └──────────────────────────┘
│ │ Flow                     │ │
│ │ ├─ run()                │ │
│ │ └─ run_async()          │ │
│ └──────────────────────────┘ │
│                              │
│ ┌──────────────────────────┐ │
│ │ Transitions              │ │
│ │ ├─ >> (default)         │ │
│ │ └─ - "condition" >>     │ │
│ └──────────────────────────┘ │
└──────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│              SPECIALIZED AGENTS                          │
│                                                          │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│ │ Research     │  │ Writer       │  │ Reviewer     │   │
│ │ Agent        │  │ Agent        │  │ Agent        │   │
│ │              │  │              │  │              │   │
│ │ - Search     │  │ - Generate   │  │ - Validate   │   │
│ │ - Analyze    │  │ - Structure  │  │ - Improve    │   │
│ │ - Summarize  │  │ - Format     │  │ - Approve    │   │
│ └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                          │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│ │ Coder        │  │ Translator   │  │ Summarizer   │   │
│ │ Agent        │  │ Agent        │  │ Agent        │   │
│ │              │  │              │  │              │   │
│ │ - Generate   │  │ - Translate  │  │ - Condense   │   │
│ │ - Test       │  │ - Validate   │  │ - Extract    │   │
│ │ - Document   │  │ - Optimize   │  │ - Highlight  │   │
│ └──────────────┘  └──────────────┘  └──────────────┘   │
└──────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│            EXTERNAL INTEGRATIONS                         │
│                                                          │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│ │ LLM Clients  │  │ MCP Tools    │  │ Databases    │   │
│ │              │  │              │  │              │   │
│ │ • OpenAI     │  │ • Web Search │  │ • PostgreSQL │   │
│ │ • Anthropic  │  │ • Code Exec  │  │ • Redis      │   │
│ │ • Google     │  │ • File I/O   │  │ • Qdrant     │   │
│ │ • Ollama     │  │ • Custom     │  │              │   │
│ └──────────────┘  └──────────────┘  └──────────────┘   │
└──────────────────────────────────────────────────────────┘
```

## 🔄 Flux de Données Complet

### Scénario 1: Créer un Agent via Builder

```
1. Utilisateur envoie requête
   │
   └─→ POST /api/v1/builder/execute
       {
         "request": "Crée un nouvel agent TranslatorAgent",
         "context": { "language": "français" }
       }
   
2. API reçoit la requête
   │
   └─→ Crée une instance AgentBuilder()
       Prépare le contexte partagé
   
3. AgentBuilder.run(shared)
   │
   ├─→ prep()
   │   └─ Extrait: "Crée un nouvel agent TranslatorAgent"
   │
   ├─→ exec()
   │   └─ Appel LLM avec le prompt
   │      LLM retourne:
   │      {
   │        "action": "create_agent",
   │        "parameters": {
   │          "name": "TranslatorAgent",
   │          "description": "Agent de traduction"
   │        }
   │      }
   │
   └─→ post()
       └─ Exécute _execute_create()
          Retourne:
          {
            "status": "created",
            "type": "agent",
            "name": "TranslatorAgent",
            "id": "agent_translatoragent"
          }

4. Réponse API
   └─→ {
         "status": "executed",
         "action": "create_agent",
         "result": { ... },
         "error": null
       }
```

### Scénario 2: Exécuter un Workflow

```
1. Utilisateur envoie requête
   │
   └─→ POST /api/v1/workflows/{workflow_id}/execute
       {
         "input_data": { "query": "Écris un article sur l'IA" },
         "async_mode": false
       }

2. API reçoit la requête
   │
   └─→ Récupère le workflow
       Crée une exécution
   
3. Workflow Engine exécute le flow
   │
   ├─→ [ResearchAgent]
   │   ├─ prep() → Extrait la requête
   │   ├─ exec() → Appel LLM (recherche)
   │   └─ post() → Stocke résultats, retourne "write"
   │
   ├─→ [WriterAgent]
   │   ├─ prep() → Récupère résultats recherche
   │   ├─ exec() → Appel LLM (rédaction)
   │   └─ post() → Stocke draft, retourne "review"
   │
   └─→ [ReviewerAgent]
       ├─ prep() → Récupère le draft
       ├─ exec() → Appel LLM (révision)
       └─ post() → Approuve ou boucle

4. Résultat final
   └─→ {
         "status": "COMPLETED",
         "output_data": {
           "final_content": "Article complet..."
         }
       }
```

### Scénario 3: Créer un Workflow avec Builder

```
1. Utilisateur
   │
   └─→ "Crée un workflow qui enchaîne ResearchAgent -> WriterAgent"

2. AgentBuilder
   │
   ├─ prep() → Extrait la requête
   │
   ├─ exec() → Appel LLM
   │   LLM retourne:
   │   {
   │     "action": "create_workflow",
   │     "parameters": {
   │       "name": "ContentPipeline",
   │       "nodes": [
   │         {"id": "research", "type": "ResearchAgent"},
   │         {"id": "writer", "type": "WriterAgent"}
   │       ],
   │       "edges": [
   │         {"from": "research", "to": "writer"}
   │       ]
   │     }
   │   }
   │
   └─ post() → Exécute _execute_create()
      Crée le workflow
      Retourne:
      {
        "status": "created",
        "type": "workflow",
        "name": "ContentPipeline",
        "id": "workflow_contentpipeline"
      }

3. Workflow est maintenant disponible
   │
   └─→ POST /api/v1/workflows/{workflow_id}/execute
```

## 🎯 Cas d'Usage Avancés

### Cas 1: Pipeline Complet

```
Frontend
  │
  ├─→ Builder: "Crée un agent Translator"
  │   └─→ Agent créé
  │
  ├─→ Builder: "Crée un workflow Research->Write->Translate->Review"
  │   └─→ Workflow créé
  │
  └─→ Execute: Workflow avec input
      └─→ Résultat final
```

### Cas 2: Gestion Dynamique

```
Monitoring
  │
  ├─→ Détecte performance faible
  │
  └─→ Builder: "Augmente température du WriterAgent à 0.9"
      └─→ Agent mis à jour
```

### Cas 3: Multi-Agents Orchestration

```
Builder
  │
  ├─→ Crée 5 agents spécialisés
  ├─→ Crée 3 workflows
  ├─→ Configure les transitions
  │
  └─→ Workflow Engine
      └─→ Exécute tous les workflows en parallèle
```

## 📊 Matrice de Responsabilités

| Composant | Création | Modification | Suppression | Exécution | Monitoring |
|-----------|----------|--------------|-------------|-----------|-----------|
| **API** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Builder** | ✅ | ✅ | ✅ | - | - |
| **Flow** | - | - | - | ✅ | ✅ |
| **Agents** | - | - | - | ✅ | ✅ |
| **Tools** | - | - | - | ✅ | - |

## 🔐 Sécurité et Validation

```
Requête Utilisateur
  │
  ├─→ Validation API
  │   └─ Vérifier format JSON
  │
  ├─→ Validation Builder
  │   └─ Vérifier action valide
  │
  ├─→ Validation Exécution
  │   └─ Vérifier paramètres
  │
  └─→ Exécution Sécurisée
      └─ Pas de code arbitraire
```

## 🚀 Performance

- **Synchrone**: Réponse immédiate
- **Asynchrone**: Exécution en arrière-plan
- **Parallèle**: Traitement de plusieurs agents
- **Cache**: Redis pour les résultats fréquents

## 📈 Scalabilité

```
Single Instance
  └─→ 100 agents, 50 workflows

Distributed
  ├─→ Multiple API instances
  ├─→ PostgreSQL pour persistence
  ├─→ Redis pour cache
  └─→ Qdrant pour vectors
```

## 🔗 Intégrations

- **Frontend**: React/Vue/Svelte
- **Database**: PostgreSQL
- **Cache**: Redis
- **Vectors**: Qdrant
- **LLMs**: OpenAI, Anthropic, Google, Ollama
- **Tools**: MCP Protocol
