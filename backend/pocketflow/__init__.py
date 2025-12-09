"""
PocketFlow - Framework minimaliste d'orchestration d'agents (~100 lignes)

Ce module fournit les primitives de base pour orchestrer des agents IA:
- Node: Unité de base avec prep/exec/post
- Flow: Orchestration de nodes avec transitions conditionnelles
- BatchNode: Traitement par lots
- AsyncNode: Support asynchrone
"""

from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
import asyncio
import time


class Node(ABC):
    """Unité de base - chaque agent hérite de Node"""
    
    def __init__(self, max_retries: int = 3, wait: int = 1):
        self.max_retries = max_retries
        self.wait = wait
        self.cur_retry = 0
        self.successors: Dict[str, "Node"] = {}
    
    def prep(self, shared: Dict) -> Any:
        """Prépare les données depuis le store partagé"""
        return None
    
    @abstractmethod
    def exec(self, prep_res: Any) -> Any:
        """Exécute la logique principale"""
        pass
    
    def post(self, shared: Dict, prep_res: Any, exec_res: Any) -> str:
        """Post-traite et retourne l'action suivante"""
        return "default"
    
    def _exec_with_retry(self, prep_res: Any) -> Any:
        """Exécute avec retry automatique"""
        for attempt in range(self.max_retries + 1):
            try:
                return self.exec(prep_res)
            except Exception as e:
                self.cur_retry = attempt + 1
                if attempt == self.max_retries:
                    raise e
                time.sleep(self.wait * (2 ** attempt))  # Backoff exponentiel
    
    def run(self, shared: Dict) -> str:
        """Exécute le node complet"""
        prep_res = self.prep(shared)
        exec_res = self._exec_with_retry(prep_res)
        return self.post(shared, prep_res, exec_res)
    
    def __rshift__(self, other: "Node") -> "Node":
        """Opérateur >> pour connexion par défaut"""
        self.successors["default"] = other
        return other
    
    def __sub__(self, condition: str) -> "_ConditionalTransition":
        """Opérateur - pour début de connexion conditionnelle"""
        return _ConditionalTransition(self, condition)


class _ConditionalTransition:
    """Helper pour les transitions conditionnelles"""
    
    def __init__(self, source: Node, condition: str):
        self.source = source
        self.condition = condition
    
    def __rshift__(self, target: Node) -> Node:
        """Opérateur >> pour compléter la connexion conditionnelle"""
        self.source.successors[self.condition] = target
        return target


class AsyncNode(Node):
    """Node asynchrone pour opérations I/O"""
    
    async def prep_async(self, shared: Dict) -> Any:
        return self.prep(shared)
    
    async def exec_async(self, prep_res: Any) -> Any:
        return self.exec(prep_res)
    
    async def post_async(self, shared: Dict, prep_res: Any, exec_res: Any) -> str:
        return self.post(shared, prep_res, exec_res)
    
    async def run_async(self, shared: Dict) -> str:
        prep_res = await self.prep_async(shared)
        exec_res = await self.exec_async(prep_res)
        return await self.post_async(shared, prep_res, exec_res)


class BatchNode(Node):
    """Node pour traitement par lots"""
    
    def exec(self, items: List[Any]) -> List[Any]:
        """Exécute pour chaque item"""
        return [self.exec_item(item) for item in items]
    
    def exec_item(self, item: Any) -> Any:
        """Override pour traiter un item"""
        raise NotImplementedError


class AsyncParallelBatchNode(AsyncNode):
    """Node pour traitement parallèle asynchrone"""
    
    async def exec_async(self, items: List[Any]) -> List[Any]:
        tasks = [self.exec_item_async(item) for item in items]
        return await asyncio.gather(*tasks)
    
    async def exec_item_async(self, item: Any) -> Any:
        raise NotImplementedError


class Flow:
    """Orchestrateur de nodes"""
    
    def __init__(self, start: Node):
        self.start = start
    
    def run(self, shared: Dict) -> Dict:
        """Exécute le flow de manière synchrone"""
        current = self.start
        
        while current is not None:
            action = current.run(shared)
            current = current.successors.get(action)
        
        return shared
    
    async def run_async(self, shared: Dict) -> Dict:
        """Exécute le flow de manière asynchrone"""
        current = self.start
        
        while current is not None:
            if isinstance(current, AsyncNode):
                action = await current.run_async(shared)
            else:
                action = current.run(shared)
            current = current.successors.get(action)
        
        return shared


# Exports
__all__ = [
    "Node",
    "AsyncNode", 
    "BatchNode",
    "AsyncParallelBatchNode",
    "Flow",
]
