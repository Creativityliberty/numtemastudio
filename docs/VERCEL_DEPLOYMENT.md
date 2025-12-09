# 🚀 Vercel Deployment Guide

## Configuration Vercel avec Token

### Votre Token Vercel
```
KLhneBoEe2dZI55hkFv4qrHa
```

## 1. Installer Vercel CLI

```bash
npm install -g vercel
```

## 2. Authentifier avec Vercel

```bash
vercel login --token KLhneBoEe2dZI55hkFv4qrHa
```

## 3. Déployer sur Vercel

### Option A: Depuis le dossier du projet

```bash
cd /Volumes/Numtema/Agentsstudio/numtema-agents-studio
vercel --prod
```

### Option B: Avec le token directement

```bash
vercel deploy --prod --token KLhneBoEe2dZI55hkFv4qrHa
```

## Configuration Automatique

Vercel détectera automatiquement:
- ✅ Frontend React (Vite)
- ✅ Backend FastAPI (Python)
- ✅ Variables d'environnement

## Variables d'Environnement à Configurer

Sur le dashboard Vercel, ajouter:

```
REACT_APP_API_URL=https://numtemastudio.vercel.app/api/v1
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

## Structure du Déploiement

```
vercel.json
├── Frontend Build
│   └── frontend/ → dist/
├── Backend Build
│   └── api/index.py → FastAPI
└── Routes
    ├── /api/* → FastAPI
    └── /* → Frontend SPA
```

## Fichiers Créés

### 1. `vercel.json` ✅
Configuration Vercel pour monorepo (frontend + backend)

### 2. `api/index.py` ✅
Entry point FastAPI pour Vercel
- Inclut les routes du backend
- Sert les fichiers statiques du frontend
- Gère le routing SPA

### 3. `requirements.txt` ✅
Dépendances Python pour Vercel

## Vérifier le Déploiement

### Après le déploiement:

```bash
# Voir le status
vercel status

# Voir les logs
vercel logs

# Voir les détails
vercel inspect
```

### Tester l'API

```bash
# Health check
curl https://numtemastudio.vercel.app/api/health

# Lister les agents
curl https://numtemastudio.vercel.app/api/v1/agents
```

### Tester le Frontend

```
https://numtemastudio.vercel.app
```

## Commandes Utiles

```bash
# Voir les deployments
vercel list

# Redéployer
vercel --prod

# Voir les variables
vercel env ls

# Ajouter une variable
vercel env add VARIABLE_NAME

# Supprimer une variable
vercel env rm VARIABLE_NAME

# Voir les logs en temps réel
vercel logs --follow
```

## Troubleshooting

### Erreur: "Module not found"
- Vérifier que `requirements.txt` est à jour
- Vérifier les imports dans `api/index.py`
- Redéployer

### Erreur: "CORS blocked"
- CORS est déjà configuré dans `api/index.py`
- Vérifier que `REACT_APP_API_URL` est correct

### Erreur: "Frontend not found"
- S'assurer que `npm run build` a été exécuté
- Vérifier que `frontend/dist/` existe
- Redéployer

### Erreur: "Environment variables not found"
- Ajouter les variables dans le dashboard Vercel
- Redéployer après avoir ajouté les variables

## Dashboard Vercel

Accéder au dashboard:
```
https://vercel.com/dashboard
```

Configurer:
1. Sélectionner le projet `numtemastudio`
2. Aller dans "Settings"
3. Ajouter les variables d'environnement
4. Redéployer si nécessaire

## Liens Utiles

- [Vercel Dashboard](https://vercel.com/dashboard)
- [Vercel FastAPI Documentation](https://vercel.com/docs/frameworks/fastapi)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

## Checklist de Déploiement

- [ ] Vercel CLI installé
- [ ] Token Vercel configuré
- [ ] `vercel.json` configuré ✅
- [ ] `api/index.py` créé ✅
- [ ] `requirements.txt` créé ✅
- [ ] Code poussé sur GitHub ✅
- [ ] Variables d'environnement ajoutées
- [ ] Déploiement lancé
- [ ] Frontend accessible
- [ ] API fonctionnelle
- [ ] Tests passants

## Prochaines Étapes

1. **Ajouter les variables d'environnement**
   ```bash
   vercel env add REACT_APP_API_URL
   vercel env add OPENAI_API_KEY
   vercel env add ANTHROPIC_API_KEY
   vercel env add GOOGLE_API_KEY
   ```

2. **Déployer**
   ```bash
   vercel --prod
   ```

3. **Vérifier**
   ```bash
   vercel logs --follow
   ```

4. **Tester**
   - Visiter https://numtemastudio.vercel.app
   - Tester l'API
   - Vérifier les logs

---

**Status**: Prêt pour le déploiement ✅
**Token**: Configuré ✅
**Frontend**: Prêt ✅
**Backend**: Prêt ✅
**Version**: 1.0.0
