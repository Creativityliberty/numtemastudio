"""
Outils MCP pour Nümtema Agents Studio

Serveur MCP et outils standards:
- web_search: Recherche web
- calculator: Calculs mathématiques
- file_ops: Opérations fichiers
- database: Requêtes base de données
- builder_tools: Gestion des agents et workflows
"""

import os
import ast
from typing import Dict, Any, Optional, Callable, List
from pathlib import Path
from .builder_tools import register_builder_tools


# =============================================================================
# TOOL REGISTRY
# =============================================================================

class ToolRegistry:
    """Registre central des outils"""
    
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._implementations: Dict[str, Callable] = {}
    
    def register(
        self, 
        name: str, 
        func: Callable,
        description: str = "",
        category: str = "general",
        input_schema: Optional[Dict] = None,
        output_schema: Optional[Dict] = None
    ):
        """Enregistre un outil"""
        self._tools[name] = {
            "name": name,
            "description": description or func.__doc__ or "",
            "category": category,
            "input_schema": input_schema or {},
            "output_schema": output_schema or {}
        }
        self._implementations[name] = func
    
    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Récupère la définition d'un outil"""
        return self._tools.get(name)
    
    def execute(self, name: str, **kwargs) -> Any:
        """Exécute un outil"""
        if name not in self._implementations:
            raise ValueError(f"Outil inconnu: {name}")
        return self._implementations[name](**kwargs)
    
    def list_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Liste les outils disponibles"""
        tools = list(self._tools.values())
        if category:
            tools = [t for t in tools if t["category"] == category]
        return tools
    
    def tool(
        self,
        name: Optional[str] = None,
        description: str = "",
        category: str = "general"
    ):
        """Décorateur pour enregistrer un outil"""
        def decorator(func: Callable) -> Callable:
            tool_name = name or func.__name__
            self.register(
                tool_name,
                func,
                description=description or func.__doc__ or "",
                category=category
            )
            return func
        return decorator


# Registre global
tool_registry = ToolRegistry()


# =============================================================================
# OUTILS STANDARDS
# =============================================================================

@tool_registry.tool(
    name="web_search",
    description="Recherche sur le web via API",
    category="search"
)
def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Recherche sur le web"""
    # Implémentation avec httpx (mock pour l'exemple)
    # En production: utiliser Brave API, SerpAPI, etc.
    return {
        "query": query,
        "results": [
            {"title": f"Result {i+1} for '{query}'", "url": f"https://example.com/{i}"}
            for i in range(max_results)
        ],
        "total": max_results
    }


@tool_registry.tool(
    name="calculator",
    description="Évalue une expression mathématique de manière sécurisée",
    category="calculation"
)
def calculator(expression: str) -> Dict[str, Any]:
    """Calculatrice sécurisée"""
    try:
        # Parser l'expression de manière sécurisée
        tree = ast.parse(expression, mode='eval')
        
        # Vérifier que seules les opérations mathématiques sont utilisées
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                raise ValueError("Les appels de fonction ne sont pas autorisés")
        
        # Évaluer de manière sécurisée
        result = eval(compile(tree, '<string>', 'eval'), {"__builtins__": {}})
        return {"expression": expression, "result": result, "success": True}
    except Exception as e:
        return {"expression": expression, "error": str(e), "success": False}


@tool_registry.tool(
    name="read_file",
    description="Lit le contenu d'un fichier",
    category="file"
)
def read_file(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """Lit un fichier"""
    try:
        file_path = Path(path)
        if not file_path.exists():
            return {"error": f"Fichier non trouvé: {path}", "success": False}
        
        content = file_path.read_text(encoding=encoding)
        return {
            "path": path,
            "content": content,
            "size": len(content),
            "success": True
        }
    except Exception as e:
        return {"error": str(e), "success": False}


@tool_registry.tool(
    name="write_file",
    description="Écrit du contenu dans un fichier",
    category="file"
)
def write_file(path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """Écrit dans un fichier"""
    try:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding=encoding)
        return {
            "path": path,
            "size": len(content),
            "success": True
        }
    except Exception as e:
        return {"error": str(e), "success": False}


@tool_registry.tool(
    name="list_directory",
    description="Liste le contenu d'un répertoire",
    category="file"
)
def list_directory(path: str = ".") -> Dict[str, Any]:
    """Liste un répertoire"""
    try:
        dir_path = Path(path)
        if not dir_path.exists():
            return {"error": f"Répertoire non trouvé: {path}", "success": False}
        
        items = []
        for item in dir_path.iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None
            })
        
        return {"path": path, "items": items, "count": len(items), "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


@tool_registry.tool(
    name="execute_python",
    description="Exécute du code Python de manière sécurisée",
    category="code"
)
def execute_python(code: str, timeout: int = 30) -> Dict[str, Any]:
    """Exécute du code Python"""
    import io
    import sys
    from contextlib import redirect_stdout, redirect_stderr
    
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    # Environnement restreint
    safe_globals = {
        "__builtins__": {
            "print": print,
            "len": len,
            "range": range,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "sum": sum,
            "min": min,
            "max": max,
            "sorted": sorted,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
        }
    }
    
    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(code, safe_globals)
        
        return {
            "success": True,
            "stdout": stdout_capture.getvalue(),
            "stderr": stderr_capture.getvalue()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "stdout": stdout_capture.getvalue(),
            "stderr": stderr_capture.getvalue()
        }


# =============================================================================
# MCP SERVER (FastMCP-style)
# =============================================================================

class MCPServer:
    """Serveur MCP simplifié"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.registry = ToolRegistry()
    
    def tool(self, name: Optional[str] = None, description: str = "", category: str = "general"):
        """Décorateur pour ajouter un outil au serveur"""
        return self.registry.tool(name, description, category)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """Liste tous les outils"""
        return self.registry.list_tools()
    
    def call_tool(self, name: str, **kwargs) -> Any:
        """Appelle un outil"""
        return self.registry.execute(name, **kwargs)
    
    def run(self, host: str = "0.0.0.0", port: int = 5001):
        """Lance le serveur MCP via FastAPI"""
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        import uvicorn
        
        app = FastAPI(title=self.name, description=self.description)
        
        class ToolCallRequest(BaseModel):
            name: str
            arguments: Dict[str, Any] = {}
        
        @app.get("/tools")
        def list_tools():
            return self.list_tools()
        
        @app.post("/tools/call")
        def call_tool(request: ToolCallRequest):
            try:
                result = self.call_tool(request.name, **request.arguments)
                return {"result": result}
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        uvicorn.run(app, host=host, port=port)


# Créer un serveur MCP par défaut avec les outils standards
mcp_server = MCPServer(
    name="Nümtema Tools",
    description="Outils standards pour le studio d'agents"
)

# Enregistrer les outils standards dans le serveur MCP
for tool_name in ["web_search", "calculator", "read_file", "write_file", 
                  "list_directory", "execute_python"]:
    tool_def = tool_registry.get(tool_name)
    if tool_def:
        mcp_server.registry.register(
            tool_name,
            tool_registry._implementations[tool_name],
            description=tool_def["description"],
            category=tool_def["category"]
        )


# =============================================================================
# REGISTER BUILDER TOOLS
# =============================================================================

register_builder_tools(tool_registry)


__all__ = [
    "ToolRegistry",
    "tool_registry",
    "MCPServer",
    "mcp_server",
    "web_search",
    "calculator",
    "read_file",
    "write_file",
    "list_directory",
    "execute_python",
    "register_builder_tools",
]
