# 🚀 Guide de Déploiement

## 1. Initialiser Git & GitHub

### Créer un repository GitHub

1. Aller sur [github.com](https://github.com)
2. Cliquer sur "New repository"
3. Nommer le repository: `numtema-agents-studio`
4. Ajouter une description
5. Choisir "Public" ou "Private"
6. Cliquer sur "Create repository"

### Initialiser Git localement

```bash
cd /Volumes/Numtema/Agentsstudio/numtema-agents-studio

# Initialiser le repository
git init

# Ajouter tous les fichiers
git add .

# Commit initial
git commit -m "Initial commit: Nümtema Agents Studio v1.0"

# Renommer la branche en main
git branch -M main

# Ajouter le remote (remplacer USERNAME et REPO)
git remote add origin https://github.com/USERNAME/numtema-agents-studio.git

# Pousser vers GitHub
git push -u origin main
```

## 2. Déployer le Frontend sur Vercel

### Option A: Via Vercel CLI

```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter à Vercel
vercel login

# Déployer depuis le dossier frontend
cd frontend
vercel
```

### Option B: Via Dashboard Vercel

1. Aller sur [vercel.com](https://vercel.com)
2. Cliquer sur "Add New..." → "Project"
3. Importer le repository GitHub
4. Sélectionner le dossier `frontend` comme root
5. Configurer les variables d'environnement:
   ```
   REACT_APP_API_URL=https://your-backend-api.com/api/v1
   ```
6. Cliquer sur "Deploy"

### Configuration Vercel

**Framework Preset**: Vite
**Build Command**: `npm run build`
**Output Directory**: `dist`
**Install Command**: `npm install`

## 3. Déployer le Backend

### Option A: Railway

```bash
# 1. Installer Railway CLI
npm i -g @railway/cli

# 2. Se connecter
railway login

# 3. Créer un nouveau projet
railway init

# 4. Ajouter les variables d'environnement
railway variables set OPENAI_API_KEY=...
railway variables set DATABASE_URL=...

# 5. Déployer
railway up
```

### Option B: Render

1. Aller sur [render.com](https://render.com)
2. Cliquer sur "New +" → "Web Service"
3. Connecter le repository GitHub
4. Configurer:
   - **Name**: numtema-agents-studio-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT`
5. Ajouter les variables d'environnement
6. Cliquer sur "Create Web Service"

### Option C: Heroku

```bash
# 1. Installer Heroku CLI
brew tap heroku/brew && brew install heroku

# 2. Se connecter
heroku login

# 3. Créer une app
heroku create numtema-agents-studio-api

# 4. Ajouter les variables
heroku config:set OPENAI_API_KEY=...

# 5. Déployer
git push heroku main
```

## 4. Configuration des Variables d'Environnement

### Frontend (Vercel)

```
REACT_APP_API_URL=https://your-backend-api.com/api/v1
```

### Backend

```
# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Database (optionnel)
DATABASE_URL=postgresql://user:password@host:port/db
REDIS_URL=redis://user:password@host:port

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## 5. Vérifier le Déploiement

### Frontend
```bash
# Visiter l'URL Vercel
https://numtema-agents-studio.vercel.app

# Vérifier la console
# Ouvrir DevTools (F12)
# Vérifier que l'API URL est correcte
```

### Backend
```bash
# Tester l'API
curl https://your-backend-api.com/api/v1/agents

# Vérifier les logs
# Aller sur le dashboard du service (Railway, Render, Heroku)
```

## 6. Mettre à Jour le Déploiement

### Frontend
```bash
# Faire les changements
git add .
git commit -m "Update frontend"
git push origin main

# Vercel déploiera automatiquement
```

### Backend
```bash
# Faire les changements
git add .
git commit -m "Update backend"
git push origin main

# Railway/Render/Heroku déploiera automatiquement
```

## 7. Dépannage

### Frontend ne se charge pas
- Vérifier que `REACT_APP_API_URL` est correcte
- Vérifier les logs Vercel
- Vérifier la console du navigateur (F12)

### API retourne des erreurs
- Vérifier que le backend est en ligne
- Vérifier les variables d'environnement
- Vérifier les logs du backend

### CORS errors
- Ajouter le domaine frontend à `ALLOWED_ORIGINS` dans le backend
- Vérifier les headers CORS

## 📋 Checklist de Déploiement

- [ ] Repository GitHub créé
- [ ] Code poussé sur GitHub
- [ ] Frontend déployé sur Vercel
- [ ] Backend déployé (Railway/Render/Heroku)
- [ ] Variables d'environnement configurées
- [ ] API URL correcte dans le frontend
- [ ] Tests de l'application
- [ ] Domaine personnalisé (optionnel)
- [ ] SSL/HTTPS activé
- [ ] Monitoring configuré

## 🔗 Liens Utiles

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Heroku Documentation](https://devcenter.heroku.com)
- [GitHub Documentation](https://docs.github.com)

---

**Status**: Prêt pour le déploiement
**Version**: 1.0.0
