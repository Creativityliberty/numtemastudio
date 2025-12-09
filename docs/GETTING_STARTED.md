# 🚀 Getting Started - Nümtema Agents Studio

## 📋 Vue d'ensemble

Bienvenue dans **Nümtema Agents Studio** - un framework complet pour construire, gérer et orchestrer des agents IA.

Ce guide vous aidera à démarrer rapidement.

## 🎯 Avant de Commencer

### Prérequis
- Python 3.10+
- Node.js 16+
- npm ou yarn
- Git

### Vérifier les installations
```bash
python --version      # Python 3.10+
node --version        # Node 16+
npm --version         # npm 8+
git --version         # Git 2.30+
```

## 📁 Structure du Projet

```
numtema-agents-studio/
├── backend/          # API Python (FastAPI)
├── frontend/         # UI React (TypeScript)
├── docs/             # Documentation
└── README.md         # Guide principal
```

## 🏃 Quick Start (5 minutes)

### 1. Cloner le Repository
```bash
git clone https://github.com/YOUR_USERNAME/numtema-agents-studio.git
cd numtema-agents-studio
```

### 2. Démarrer le Backend
```bash
# Créer un virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -e .

# Démarrer le serveur
python -m uvicorn backend.api.main:app --reload
```

Backend disponible sur: **http://localhost:8000**

### 3. Démarrer le Frontend
```bash
cd frontend

# Installer les dépendances
npm install

# Démarrer le dev server
npm run dev
```

Frontend disponible sur: **http://localhost:3000**

## 🎨 Fonctionnalités Principales

### Dashboard
- Vue d'ensemble avec statistiques
- Agents récents
- Quick actions
- System status

### Agents
- Créer, lire, mettre à jour, supprimer
- Recherche et filtrage
- Duplication
- Gestion des statuts

### Workflows
- Éditeur visuel
- Drag-and-drop nodes
- Exécution
- Historique

### Builder
- Chat interface
- Création d'agents par conversation
- Historique des actions
- Quick actions

### Settings
- Configuration API
- Thème
- Notifications
- Sécurité

## 📚 Documentation

### Navigation
- **[INDEX.md](./INDEX.md)** - Guide de navigation complet
- **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - Status global
- **[PHASE_1_COMPLETE.md](./PHASE_1_COMPLETE.md)** - Components
- **[PHASE_2_COMPLETE.md](./PHASE_2_COMPLETE.md)** - Pages
- **[PHASE_3_COMPLETE.md](./PHASE_3_COMPLETE.md)** - Integration

### Architecture
- **[FRONTEND_PLAN.md](./FRONTEND_PLAN.md)** - Plan détaillé frontend
- **[architecture_with_builder.md](./architecture_with_builder.md)** - Architecture complète
- **[AGENT_BUILDER_SUMMARY.md](./AGENT_BUILDER_SUMMARY.md)** - Agent Builder

### Déploiement
- **[../DEPLOYMENT.md](../DEPLOYMENT.md)** - Guide de déploiement
- **[../ORGANIZATION.md](../ORGANIZATION.md)** - Organisation du projet

## 🔧 Configuration

### Variables d'Environnement

Créer un fichier `.env` à la racine:

```bash
cp .env.example .env
```

Configurer les variables:

```env
# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# API
API_HOST=0.0.0.0
API_PORT=8000

# Frontend
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 🧪 Tester l'Application

### Backend API
```bash
# Lister les agents
curl http://localhost:8000/api/v1/agents

# Créer un agent
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "description": "A test agent",
    "type": "Research"
  }'
```

### Frontend
1. Ouvrir http://localhost:3000
2. Naviguer vers différentes pages
3. Tester les fonctionnalités

## 🚀 Déployer

### Frontend sur Vercel

1. Pousser le code sur GitHub
2. Aller sur https://vercel.com
3. Importer le repository
4. Sélectionner le dossier `frontend`
5. Configurer les variables d'environnement
6. Déployer

Voir **[DEPLOYMENT.md](../DEPLOYMENT.md)** pour plus de détails.

### Backend

Voir **[DEPLOYMENT.md](../DEPLOYMENT.md)** pour les options (Railway, Render, Heroku).

## 📖 Apprendre Plus

### Concepts Clés

**Agents**
- Unités autonomes qui exécutent des tâches
- Peuvent être créés via l'interface ou l'API
- Supportent différents types (Research, Writer, Coder, etc.)

**Workflows**
- Orchestration de plusieurs agents
- Éditeur visuel avec drag-and-drop
- Exécution asynchrone

**Builder**
- Interface chat pour créer des agents
- Utilise l'Agent Builder du backend
- Gère les MCP Tools

**MCP Tools**
- Model Context Protocol
- 10 outils CRUD intégrés
- Extensibles

### Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Zustand](https://github.com/pmndrs/zustand)

## ❓ Troubleshooting

### Frontend ne se charge pas
- Vérifier que le backend est en ligne
- Vérifier la console du navigateur (F12)
- Vérifier que `REACT_APP_API_URL` est correcte

### API retourne des erreurs
- Vérifier les logs du backend
- Vérifier les variables d'environnement
- Vérifier la base de données

### Erreurs TypeScript
- Exécuter `npm run type-check`
- Vérifier les imports
- Vérifier les types

## 📞 Support

- Consultez la documentation dans `docs/`
- Ouvrez une issue sur GitHub
- Vérifiez les exemples dans `backend/examples/`

## ✅ Checklist de Démarrage

- [ ] Repository cloné
- [ ] Python 3.10+ installé
- [ ] Node.js 16+ installé
- [ ] Virtual environment créé
- [ ] Dépendances installées
- [ ] Variables d'environnement configurées
- [ ] Backend démarré (http://localhost:8000)
- [ ] Frontend démarré (http://localhost:3000)
- [ ] Testes les fonctionnalités
- [ ] Prêt pour le déploiement

## 🎉 Prochaines Étapes

1. **Explorer l'Application**
   - Visiter le Dashboard
   - Créer un agent
   - Créer un workflow
   - Utiliser le Builder

2. **Lire la Documentation**
   - Commencer par [INDEX.md](./INDEX.md)
   - Lire les phases complétées
   - Comprendre l'architecture

3. **Déployer**
   - Suivre [DEPLOYMENT.md](../DEPLOYMENT.md)
   - Configurer GitHub
   - Déployer sur Vercel

4. **Personnaliser**
   - Modifier les couleurs
   - Ajouter des agents
   - Créer des workflows

---

**Version**: 1.0.0
**Status**: Production Ready
**Last Updated**: Décembre 2025

**Besoin d'aide?** Consultez la documentation complète dans le dossier `docs/`
