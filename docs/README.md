# Nümtema Agents Studio

Studio d'Agents IA basé sur PocketFlow — Framework Minimaliste (~100 lignes)

## 🎯 Philosophie

- **Minimalisme** : PocketFlow en ~100 lignes, contrôle total
- **Zéro magie cachée** : Chaque ligne de code est compréhensible
- **Type-Safety** : Validation stricte avec Pydantic
- **Protocoles standards** : MCP pour l'interopérabilité

## 🏗️ Architecture

```
numtema-agents-studio/
├── pocketflow/           # Core framework (~100 lignes)
├── agents/               # Agents spécialisés
├── tools/                # Outils MCP
├── workflows/            # Moteur de workflow
├── models/               # Modèles Pydantic
├── utils/                # Utilitaires (LLM client)
├── api/                  # API FastAPI
└── tests/                # Tests
```

## 🚀 Démarrage Rapide

### 1. Installation

```bash
# Cloner le repository
git clone https://github.com/numtema/agents-studio.git
cd numtema-agents-studio

# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -e ".[dev]"

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos clés API
```

### 2. Lancer avec Docker

```bash
docker compose up -d
```

### 3. Lancer en développement

```bash
# API
uvicorn api.main:app --reload

# L'API est disponible sur http://localhost:8000
# Documentation: http://localhost:8000/docs
```

## 📚 Concepts Clés

### PocketFlow - Le Cœur

```python
from pocketflow import Node, Flow

class MyAgent(Node):
    def prep(self, shared):
        return shared.get("query")
    
    def exec(self, query):
        return process(query)
    
    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res
        return "next"  # Action suivante

# Connexions
agent1 >> agent2 >> agent3
agent1 - "condition" >> agent_alt

# Exécution
flow = Flow(start=agent1)
result = flow.run({"query": "Hello"})
```

### Agents Spécialisés

```python
from agents import ResearchAgent, WriterAgent, ReviewerAgent

# Pipeline de contenu
researcher = ResearchAgent()
writer = WriterAgent()
reviewer = ReviewerAgent()

researcher - "write" >> writer
writer - "review" >> reviewer
reviewer - "write" >> writer  # Boucle de révision

flow = Flow(start=researcher)
result = flow.run({"query": "IA en 2025"})
```

### API Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/v1/agents` | GET/POST | Gestion des agents |
| `/api/v1/workflows` | GET/POST | Gestion des workflows |
| `/api/v1/workflows/{id}/execute` | POST | Exécution |
| `/api/v1/executions/{id}` | GET | Statut d'exécution |
| `/api/v1/tools` | GET | Liste des outils |

## 🔧 Configuration

### Variables d'environnement

```bash
# LLM Provider
LLM_PROVIDER=openai  # openai, anthropic, google, ollama
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379/0
```

## 🧪 Tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=. --cov-report=html
```

## 📖 Documentation

- [Architecture Complète](docs/architecture.md)
- [Guide des Agents](docs/agents.md)
- [API Reference](docs/api.md)

## 🤝 Contribuer

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

## 📄 Licence

Apache 2.0 - Voir [LICENSE](LICENSE)

---

**Nümtema** — Studio d'Agents IA de nouvelle génération
