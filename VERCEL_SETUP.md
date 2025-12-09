# 🚀 Configuration Vercel - Étapes Finales

## ✅ Votre Token Vercel

```
KLhneBoEe2dZI55hkFv4qrHa
```

## 📋 Configuration via Dashboard Vercel

### Étape 1: Aller sur Vercel Dashboard

```
https://vercel.com/dashboard
```

### Étape 2: Sélectionner le Projet

Cliquer sur `numtema-agents-studio`

### Étape 3: Aller dans Settings

Settings → Environment Variables

### Étape 4: Ajouter les Variables

Ajouter ces variables d'environnement:

```
REACT_APP_API_URL = https://numtemastudio.vercel.app/api/v1
OPENAI_API_KEY = sk-... (votre clé)
ANTHROPIC_API_KEY = sk-ant-... (votre clé)
GOOGLE_API_KEY = ... (votre clé)
```

### Étape 5: Redéployer

Cliquer sur "Deployments" → Sélectionner le dernier → "Redeploy"

## 🔗 Liens Directs

- **Dashboard**: https://vercel.com/dashboard
- **Projet**: https://vercel.com/dashboard/numtema-agents-studio
- **Deployments**: https://vercel.com/dashboard/numtema-agents-studio/deployments
- **Settings**: https://vercel.com/dashboard/numtema-agents-studio/settings

## 📝 Variables à Ajouter

### REACT_APP_API_URL
```
https://numtemastudio.vercel.app/api/v1
```

### OPENAI_API_KEY
```
sk-... (votre clé OpenAI)
```

### ANTHROPIC_API_KEY
```
sk-ant-... (votre clé Anthropic)
```

### GOOGLE_API_KEY
```
... (votre clé Google)
```

## ✅ Après Configuration

1. Ajouter les variables
2. Redéployer
3. Attendre 2-3 minutes
4. Visiter: https://numtemastudio.vercel.app

## 🎯 Vérifier le Déploiement

```bash
# Health check
curl https://numtemastudio.vercel.app/api/health

# Agents
curl https://numtemastudio.vercel.app/api/v1/agents
```

## 📞 Support

Si vous avez des erreurs:
1. Vérifier les logs dans Vercel Dashboard
2. Vérifier les variables d'environnement
3. Redéployer

---

**Status**: Prêt pour configuration finale ✅
**URL**: https://numtemastudio.vercel.app
**Token**: Configuré ✅
