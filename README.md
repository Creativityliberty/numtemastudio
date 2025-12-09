# 🤖 Nümtema Agents Studio

Un framework complet pour construire, gérer et orchestrer des agents IA avec une interface moderne et intuitive.

## 📁 Structure du Projet

```
numtema-agents-studio/
├── backend/                    # Backend Python (FastAPI)
│   ├── agents/                 # Agents spécialisés
│   ├── api/                    # API REST endpoints
│   ├── models/                 # Modèles de données
│   ├── pocketflow/             # Framework PocketFlow
│   ├── tools/                  # MCP Tools
│   ├── utils/                  # Utilitaires
│   ├── workflows/              # Workflows
│   ├── examples/               # Exemples d'utilisation
│   └── tests/                  # Tests
├── frontend/                   # Frontend React/TypeScript
│   ├── src/
│   │   ├── components/         # Composants React
│   │   ├── pages/              # Pages principales
│   │   ├── hooks/              # Custom hooks
│   │   ├── services/           # Services API
│   │   ├── store/              # Zustand stores
│   │   ├── styles/             # Styles globaux
│   │   ├── types/              # Types TypeScript
│   │   └── utils/              # Utilitaires
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs/                       # Documentation
├── pyproject.toml              # Configuration Python
├── .env.example                # Variables d'environnement
└── README.md                   # Ce fichier
```

## 🚀 Quick Start

### Backend

```bash
# Installation
pip install -r pyproject.toml

# Variables d'environnement
cp .env.example .env

# Démarrer le serveur
python -m uvicorn backend.api.main:app --reload
```

Backend disponible sur: `http://localhost:8000`

### Frontend

```bash
cd frontend

# Installation
npm install

# Development
npm run dev
```

Frontend disponible sur: `http://localhost:3000`

## 🎯 Features

### Backend
- ✅ Agent Builder avec MCP Tools
- ✅ 10 outils CRUD pour agents et workflows
- ✅ Framework PocketFlow pour orchestration
- ✅ API REST complète
- ✅ Support multi-LLM (OpenAI, Anthropic, Google, Ollama)
- ✅ Database ready (PostgreSQL, Redis, Qdrant)

### Frontend
- ✅ Dashboard avec statistiques
- ✅ Gestion des agents (CRUD)
- ✅ Éditeur de workflows (drag-and-drop)
- ✅ Chat Builder pour créer des agents
- ✅ Settings et configuration
- ✅ Design moderne avec animations
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Dark mode par défaut

## 📊 Phases Complétées

### Phase 1: Components ✅
- 11 composants créés (Button, Card, Input, Modal, Toast, Sidebar, etc.)
- Design system complet
- Animations fluides
- Responsive design

### Phase 2: Pages ✅
- 5 pages principales (Dashboard, Agents, Workflows, Builder, Settings)
- Routing complet
- Navigation fluide
- Mock data

### Phase 3: Integration ✅
- API Client avec Axios
- Services pour Agents et Workflows
- Zustand stores
- State management
- Error handling

## 🛠️ Stack Technologique

### Backend
- Python 3.10+
- FastAPI
- Pydantic
- SQLAlchemy
- Redis
- Qdrant

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Zustand
- React Query
- React Flow
- Framer Motion

## 📚 Documentation

Consultez le dossier `docs/` pour la documentation complète:

- `INDEX.md` - Guide de navigation
- `PROJECT_STATUS.md` - Status global
- `PHASE_1_COMPLETE.md` - Phase 1 (Components)
- `PHASE_2_COMPLETE.md` - Phase 2 (Pages)
- `PHASE_3_COMPLETE.md` - Phase 3 (Integration)
- `FRONTEND_PLAN.md` - Plan frontend détaillé
- `AGENT_BUILDER_SUMMARY.md` - Résumé Agent Builder
- `BUILDER_TOOLS_SUMMARY.md` - Résumé Builder Tools

## 🔌 API Endpoints

### Agents
```
POST   /api/v1/agents              # Créer un agent
GET    /api/v1/agents              # Lister les agents
GET    /api/v1/agents/{id}         # Récupérer un agent
PUT    /api/v1/agents/{id}         # Mettre à jour un agent
DELETE /api/v1/agents/{id}         # Supprimer un agent
```

### Workflows
```
POST   /api/v1/workflows           # Créer un workflow
GET    /api/v1/workflows           # Lister les workflows
GET    /api/v1/workflows/{id}      # Récupérer un workflow
PUT    /api/v1/workflows/{id}      # Mettre à jour un workflow
DELETE /api/v1/workflows/{id}      # Supprimer un workflow
```

### Builder
```
POST   /api/v1/builder/execute     # Exécuter le builder
GET    /api/v1/builder/capabilities # Récupérer les capacités
```

## 🚀 Déploiement

### Frontend sur Vercel

```bash
# 1. Créer un repository GitHub
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/numtema-agents-studio.git
git push -u origin main

# 2. Connecter à Vercel
# - Aller sur https://vercel.com
# - Importer le repository
# - Sélectionner le dossier `frontend` comme root
# - Configurer les variables d'environnement
# - Déployer

# Variables d'environnement Vercel:
REACT_APP_API_URL=https://your-backend-api.com/api/v1
```

### Backend sur Railway/Render

```bash
# 1. Préparer le backend
cd backend
pip freeze > requirements.txt

# 2. Créer un Procfile
echo "web: uvicorn api.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 3. Déployer sur Railway ou Render
```

## 🔐 Variables d'Environnement

Voir `.env.example` pour la liste complète.

### Frontend
```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Backend
```
# LLM Providers
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...

# Database
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
QDRANT_URL=http://localhost:6333

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## 📝 License

MIT License - voir LICENSE pour plus de détails

## 🤝 Contributing

Les contributions sont bienvenues! Veuillez:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📞 Support

Pour des questions ou des problèmes:
- Consultez la documentation dans `docs/`
- Ouvrez une issue sur GitHub
- Contactez l'équipe

---

**Version**: 1.0.0
**Status**: Production Ready
**Last Updated**: Décembre 2025
# numtemastudio
