# 🎨 Agent Builder Studio - Frontend

Un frontend ultra-moderne et innovant pour le Agent Builder Studio avec un design minimaliste arrondi, animations fluides et dark mode élégant.

## 🚀 Quick Start

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Le frontend sera disponible à `http://localhost:3000`

### Build

```bash
npm run build
```

### Preview

```bash
npm run preview
```

## 📦 Stack Technologique

- **React 18** - UI Framework
- **TypeScript** - Type Safety
- **Vite** - Build Tool ultra-rapide
- **Tailwind CSS** - Utility-first CSS
- **Framer Motion** - Animations fluides
- **React Router v6** - Navigation
- **Zustand** - State Management
- **React Query** - Server State
- **React Flow** - Workflow Editor
- **Lucide React** - Icons

## 🎨 Design System

### Couleurs (Dark Mode)

- **Primary**: Indigo (#6366f1)
- **Accent**: Pink (#ec4899)
- **Background**: Slate-900 (#0f172a)
- **Text**: Slate-100 (#f1f5f9)

### Formes Arrondies

- `rounded-sm`: 6px
- `rounded-md`: 8px
- `rounded-lg`: 16px
- `rounded-xl`: 24px
- `rounded-full`: Complètement arrondi

### Animations

- Fade in/out
- Slide in/out
- Scale in/out
- Pulse subtle
- Glow effects

## 📁 Structure du Projet

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/          # Composants réutilisables
│   │   ├── agents/          # Composants agents
│   │   ├── workflows/       # Composants workflows
│   │   ├── builder/         # Composants builder
│   │   └── layout/          # Layout components
│   ├── pages/               # Pages principales
│   ├── hooks/               # Custom hooks
│   ├── services/            # API services
│   ├── store/               # Zustand stores
│   ├── styles/              # CSS global
│   ├── types/               # TypeScript types
│   ├── utils/               # Utility functions
│   ├── App.tsx              # Root component
│   └── index.tsx            # Entry point
├── public/                  # Static assets
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

## 🎯 Pages Principales

### Dashboard
- Vue d'ensemble des agents et workflows
- Statistiques en temps réel
- Actions rapides
- Historique récent

### Agents Management
- Liste des agents avec cartes arrondies
- Créer/Modifier/Supprimer agents
- Détails et configuration
- Tags et catégories

### Workflows Editor
- Canvas interactif avec drag-and-drop
- Nœuds arrondis avec icônes
- Connexions fluides
- Édition en temps réel

### Agent Builder
- Chat interface pour créer agents
- Historique des actions
- Prévisualisation en temps réel
- Validation et suggestions

### Settings
- Préférences utilisateur
- Configuration API
- Thème et apparence
- Gestion des clés API

## 🔌 API Integration

Le frontend se connecte à l'API backend sur `http://localhost:8000`

### Endpoints utilisés

```
POST   /api/v1/agents              # Créer un agent
GET    /api/v1/agents              # Lister les agents
GET    /api/v1/agents/{id}         # Récupérer un agent
PUT    /api/v1/agents/{id}         # Mettre à jour un agent
DELETE /api/v1/agents/{id}         # Supprimer un agent

POST   /api/v1/workflows           # Créer un workflow
GET    /api/v1/workflows           # Lister les workflows
GET    /api/v1/workflows/{id}      # Récupérer un workflow
PUT    /api/v1/workflows/{id}      # Mettre à jour un workflow
DELETE /api/v1/workflows/{id}      # Supprimer un workflow

POST   /api/v1/builder/execute     # Exécuter le builder
GET    /api/v1/builder/capabilities # Récupérer les capacités
```

## 🎬 Animations & Interactions

### Transitions
- Page transitions (fade, slide)
- Component mount/unmount
- Hover effects (scale, glow)
- Click feedback (ripple)

### Micro-interactions
- Loading spinners (animated)
- Toast notifications (slide in/out)
- Modal animations (scale + fade)
- Skeleton loaders

### Workflow Canvas
- Smooth pan and zoom
- Node drag animations
- Connection drawing
- Auto-layout animations

## 📱 Responsive Design

- **Mobile** (< 640px): Single column, bottom navigation
- **Tablet** (640px - 1024px): Two columns, side navigation
- **Desktop** (> 1024px): Three columns, full sidebar

## 🔐 Security

- HTTPS only (production)
- CSRF protection
- XSS prevention
- Input validation
- API key management
- Rate limiting

## 📊 Performance Targets

- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s
- Cumulative Layout Shift: < 0.1
- Time to Interactive: < 3.5s
- Bundle size: < 200KB (gzipped)

## 🧪 Testing

```bash
# Unit tests
npm run test

# UI tests
npm run test:ui

# E2E tests
npm run test:e2e
```

## 📚 Documentation

- [Design System](./FRONTEND_PLAN.md)
- [Component Library](./docs/components.md)
- [API Integration](./docs/api.md)
- [State Management](./docs/store.md)

## 🚀 Deployment

### Build pour production

```bash
npm run build
```

### Deploy sur Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

### Deploy sur Vercel

```bash
npm install -g vercel
vercel --prod
```

## 🤝 Contributing

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📝 License

MIT License - voir le fichier LICENSE pour plus de détails

## 🎉 Résumé

Un frontend **ultra-moderne et innovant** avec:

✅ Design minimaliste arrondi
✅ Animations fluides
✅ Dark mode élégant
✅ Responsive design
✅ Drag-and-drop workflows
✅ Chat builder intégré
✅ Performance optimisée
✅ Entièrement typé (TypeScript)

**Prêt à être développé!** 🚀
