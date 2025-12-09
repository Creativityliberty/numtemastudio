"""
Agents pour Nümtema Agents Studio

Agents spécialisés basés sur PocketFlow:
- BaseAgent: Agent de base avec fonctionnalités enrichies
- ResearchAgent: Recherche d'information
- WriterAgent: Rédaction de contenu
- ReviewerAgent: Révision et qualité
- CoderAgent: Génération de code
"""

import yaml
from typing import Any, Dict, Optional, Callable, List

from pocketflow import Node, AsyncNode
from models import AgentConfig, LLMProvider
from utils.llm import call_llm


class BaseAgent(Node):
    """Agent de base avec fonctionnalités enrichies"""
    
    def __init__(self, config: AgentConfig, **kwargs):
        super().__init__(max_retries=config.max_retries, **kwargs)
        self.config = config
        self.tools: Dict[str, Callable] = {}
    
    @property
    def name(self) -> str:
        return self.config.name
    
    def register_tool(self, name: str, func: Callable):
        """Enregistre un outil utilisable par l'agent"""
        self.tools[name] = func
    
    def build_prompt(
        self, 
        user_input: str, 
        context: Optional[Dict] = None
    ) -> str:
        """Construit le prompt complet"""
        parts = [f"# System\n{self.config.system_prompt}"]
        
        # Ajouter les outils disponibles
        if self.tools:
            tools_desc = "\n".join([f"- {name}" for name in self.tools])
            parts.append(f"\n# Outils disponibles\n{tools_desc}")
        
        # Ajouter le contexte
        if context:
            parts.append(f"\n# Contexte\n{yaml.dump(context, allow_unicode=True)}")
        
        # Ajouter l'input utilisateur
        parts.append(f"\n# Input\n{user_input}")
        
        # Spécifier le format de sortie
        if self.config.output_format == "yaml":
            parts.append("\n# Format de sortie\nRépondez en YAML valide.")
        elif self.config.output_format == "json":
            parts.append("\n# Format de sortie\nRépondez en JSON valide.")
        
        return "\n".join(parts)
    
    def parse_output(self, raw_output: str) -> Any:
        """Parse la sortie selon le format configuré"""
        if self.config.output_format == "yaml":
            try:
                # Extraire le YAML des blocs de code si présent
                if "```yaml" in raw_output:
                    yaml_content = raw_output.split("```yaml")[1].split("```")[0]
                    return yaml.safe_load(yaml_content)
                return yaml.safe_load(raw_output)
            except yaml.YAMLError:
                return {"raw": raw_output, "parse_error": True}
        elif self.config.output_format == "json":
            import json
            try:
                if "```json" in raw_output:
                    json_content = raw_output.split("```json")[1].split("```")[0]
                    return json.loads(json_content)
                return json.loads(raw_output)
            except json.JSONDecodeError:
                return {"raw": raw_output, "parse_error": True}
        return raw_output
    
    def exec(self, prep_res: Any) -> Any:
        """Exécute l'appel LLM"""
        prompt = self.build_prompt(str(prep_res))
        raw_output = call_llm(
            prompt,
            model=self.config.model_name,
            provider=self.config.model_provider,
            temperature=self.config.temperature
        )
        return self.parse_output(raw_output)


class AsyncBaseAgent(AsyncNode):
    """Version asynchrone de BaseAgent"""
    
    def __init__(self, config: AgentConfig, **kwargs):
        super().__init__(max_retries=config.max_retries, **kwargs)
        self.config = config
        self.tools: Dict[str, Callable] = {}
    
    # Mêmes méthodes que BaseAgent...
    # (omis pour concision, identique à BaseAgent)


# =============================================================================
# AGENTS SPÉCIALISÉS
# =============================================================================

class ResearchAgent(BaseAgent):
    """Agent spécialisé en recherche d'information"""
    
    def __init__(self, **kwargs):
        config = AgentConfig(
            name="Research Agent",
            description="Agent de recherche et analyse d'information",
            system_prompt="""Vous êtes un assistant de recherche expert.
Analysez le sujet et fournissez des informations structurées.

Sortie YAML attendue:
```yaml
topic: <sujet analysé>
key_findings:
  - point 1
  - point 2
  - point 3
confidence: high/medium/low
sources_needed: true/false
summary: <résumé concis>
```""",
            output_format="yaml",
            **kwargs.get("config_overrides", {})
        )
        super().__init__(config)
    
    def prep(self, shared: Dict) -> Dict:
        return {
            "query": shared.get("query", ""),
            "history": shared.get("research_history", []),
            "constraints": shared.get("constraints", {})
        }
    
    def post(self, shared: Dict, prep_res: Any, exec_res: Any) -> str:
        # Sauvegarder les résultats
        if "research_history" not in shared:
            shared["research_history"] = []
        shared["research_history"].append(exec_res)
        shared["latest_research"] = exec_res
        
        # Décider de la prochaine action
        if isinstance(exec_res, dict):
            if exec_res.get("confidence") == "low":
                return "research"  # Continuer la recherche
            if exec_res.get("sources_needed"):
                return "search"  # Besoin de sources
        
        return "write"  # Passer à l'écriture


class WriterAgent(BaseAgent):
    """Agent spécialisé en rédaction"""
    
    def __init__(self, **kwargs):
        config = AgentConfig(
            name="Writer Agent",
            description="Agent de rédaction de contenu professionnel",
            system_prompt="""Vous êtes un rédacteur professionnel.
Créez du contenu clair, engageant et structuré basé sur la recherche fournie.

Sortie YAML attendue:
```yaml
title: <titre du contenu>
content: |
  <contenu rédigé complet>
word_count: <nombre de mots>
tone: professional/casual/academic
needs_review: true/false
sections:
  - name: <nom section>
    content: <contenu>
```""",
            output_format="yaml",
            **kwargs.get("config_overrides", {})
        )
        super().__init__(config)
    
    def prep(self, shared: Dict) -> Dict:
        return {
            "research": shared.get("latest_research", {}),
            "style_guide": shared.get("style_guide", "professional"),
            "target_length": shared.get("target_length", 1000),
            "audience": shared.get("audience", "general")
        }
    
    def post(self, shared: Dict, prep_res: Any, exec_res: Any) -> str:
        shared["draft"] = exec_res
        
        if isinstance(exec_res, dict) and exec_res.get("needs_review"):
            return "review"
        return "finalize"


class ReviewerAgent(BaseAgent):
    """Agent spécialisé en révision et qualité"""
    
    def __init__(self, **kwargs):
        config = AgentConfig(
            name="Reviewer Agent",
            description="Agent de révision et contrôle qualité",
            system_prompt="""Vous êtes un éditeur expert.
Révisez le contenu pour: précision, clarté, grammaire, complétude, cohérence.

Sortie YAML attendue:
```yaml
approved: true/false
score: <1-10>
issues:
  - issue: <description du problème>
    severity: high/medium/low
    location: <où dans le texte>
    suggestion: <correction proposée>
feedback: <feedback général>
revised_content: |
  <version révisée si non approuvé>
```""",
            output_format="yaml",
            **kwargs.get("config_overrides", {})
        )
        super().__init__(config)
    
    def prep(self, shared: Dict) -> Dict:
        draft = shared.get("draft", {})
        content = draft.get("content", str(draft)) if isinstance(draft, dict) else str(draft)
        return {
            "content": content,
            "criteria": shared.get("review_criteria", [
                "accuracy", "clarity", "grammar", "completeness"
            ]),
            "previous_reviews": shared.get("review_history", [])
        }
    
    def post(self, shared: Dict, prep_res: Any, exec_res: Any) -> str:
        # Sauvegarder la révision
        if "review_history" not in shared:
            shared["review_history"] = []
        shared["review_history"].append(exec_res)
        shared["latest_review"] = exec_res
        
        if isinstance(exec_res, dict):
            if not exec_res.get("approved", False):
                # Mettre à jour le draft avec la version révisée
                if exec_res.get("revised_content"):
                    shared["draft"] = {"content": exec_res["revised_content"]}
                return "write"  # Retourner à l'écriture
            
            # Approuvé - sauvegarder le contenu final
            shared["final_content"] = shared.get("draft", {})
        
        return "complete"


class CoderAgent(BaseAgent):
    """Agent spécialisé en génération de code"""
    
    def __init__(self, **kwargs):
        config = AgentConfig(
            name="Coder Agent",
            description="Agent de génération et analyse de code",
            system_prompt="""Vous êtes un développeur expert.
Générez du code propre, bien documenté et testé.

Sortie YAML attendue:
```yaml
language: <langage de programmation>
description: <ce que fait le code>
code: |
  <code généré>
dependencies:
  - <dépendance>
tests: |
  <tests unitaires>
notes: <notes importantes>
```""",
            output_format="yaml",
            model_name="gpt-4o",  # Meilleur pour le code
            **kwargs.get("config_overrides", {})
        )
        super().__init__(config)
    
    def prep(self, shared: Dict) -> Dict:
        return {
            "task": shared.get("coding_task", ""),
            "language": shared.get("language", "python"),
            "requirements": shared.get("requirements", []),
            "existing_code": shared.get("existing_code", "")
        }
    
    def post(self, shared: Dict, prep_res: Any, exec_res: Any) -> str:
        shared["generated_code"] = exec_res
        
        if isinstance(exec_res, dict) and exec_res.get("tests"):
            return "test"  # Exécuter les tests
        return "complete"


class AgentBuilder(BaseAgent):
    """Agent Builder - Gère la création/modification/suppression d'agents et workflows via MCP Tools"""
    
    def __init__(self, **kwargs):
        config = AgentConfig(
            name="Agent Builder",
            description="Agent spécialisé en création et gestion d'agents et workflows",
            system_prompt="""Vous êtes un expert en orchestration d'agents IA.
Vous pouvez créer, modifier, lister et supprimer des agents et workflows en utilisant les outils disponibles.

Outils disponibles (MCP):
- create_agent: Crée un nouvel agent
- update_agent: Met à jour un agent existant
- delete_agent: Supprime un agent
- list_agents: Liste tous les agents
- get_agent: Récupère les détails d'un agent
- create_workflow: Crée un nouveau workflow
- update_workflow: Met à jour un workflow
- delete_workflow: Supprime un workflow
- list_workflows: Liste tous les workflows
- get_workflow: Récupère les détails d'un workflow

Sortie JSON attendue:
```json
{
  "tool": "create_agent|update_agent|delete_agent|list_agents|get_agent|create_workflow|update_workflow|delete_workflow|list_workflows|get_workflow",
  "parameters": {
    "name": "optional - nom",
    "description": "optional - description",
    "agent_id": "optional - ID de l'agent",
    "workflow_id": "optional - ID du workflow",
    "config": "optional - configuration",
    "nodes": "optional - nœuds du workflow",
    "edges": "optional - connexions du workflow",
    "agent_type": "optional - type d'agent",
    "tags": "optional - tags"
  },
  "reason": "Explication de l'action"
}
```""",
            output_format="json",
            **kwargs.get("config_overrides", {})
        )
        super().__init__(config)
        self.tool_registry = None  # Sera injecté par le flow
    
    def register_tool_registry(self, tool_registry):
        """Enregistre le registre des outils pour les opérations CRUD"""
        self.tool_registry = tool_registry
    
    def prep(self, shared: Dict) -> Dict:
        return {
            "request": shared.get("builder_request", ""),
            "current_agents": shared.get("agents_list", []),
            "current_workflows": shared.get("workflows_list", []),
            "context": shared.get("builder_context", {})
        }
    
    def post(self, shared: Dict, prep_res: Any, exec_res: Any) -> str:
        """Post-traite la réponse et exécute l'action via les tools MCP"""
        if not isinstance(exec_res, dict):
            shared["builder_error"] = "Invalid response format"
            return "error"
        
        try:
            tool_name = exec_res.get("tool", "").lower()
            params = exec_res.get("parameters", {})
            
            # Vérifier que le registre des outils est disponible
            if not self.tool_registry:
                shared["builder_error"] = "Tool registry not initialized"
                return "error"
            
            # Exécuter le tool via le registre MCP
            result = self.tool_registry.execute(tool_name, **params)
            
            shared["builder_result"] = result
            shared["last_action"] = tool_name
            
            # Vérifier le succès
            success = result.get("success", False) if isinstance(result, dict) else False
            return "success" if success else "error"
        
        except Exception as e:
            shared["builder_error"] = str(e)
            shared["builder_result"] = {"success": False, "error": str(e)}
            return "error"


# =============================================================================
# FACTORY
# =============================================================================

AGENT_REGISTRY: Dict[str, type] = {
    "research": ResearchAgent,
    "writer": WriterAgent,
    "reviewer": ReviewerAgent,
    "coder": CoderAgent,
    "builder": AgentBuilder,
}


def create_agent(agent_type: str, **kwargs) -> BaseAgent:
    """Factory pour créer des agents par type"""
    if agent_type not in AGENT_REGISTRY:
        raise ValueError(f"Type d'agent inconnu: {agent_type}. "
                        f"Disponibles: {list(AGENT_REGISTRY.keys())}")
    return AGENT_REGISTRY[agent_type](**kwargs)


def register_agent_type(name: str, agent_class: type):
    """Enregistre un nouveau type d'agent"""
    AGENT_REGISTRY[name] = agent_class


__all__ = [
    "BaseAgent",
    "AsyncBaseAgent",
    "ResearchAgent",
    "WriterAgent", 
    "ReviewerAgent",
    "CoderAgent",
    "AgentBuilder",
    "create_agent",
    "register_agent_type",
    "AGENT_REGISTRY",
]
