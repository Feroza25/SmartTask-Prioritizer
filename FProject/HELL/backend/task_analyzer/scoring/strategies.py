from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List
import math

class ScoringStrategy(ABC):
    """Abstract base class for all scoring strategies"""
    
    @abstractmethod
    def calculate_score(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        pass
    
    def get_strategy_name(self) -> str:
        return self.__class__.__name__

class FastestWinsStrategy(ScoringStrategy):
    """Prioritize tasks that can be completed quickly"""
    
    def calculate_score(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        effort = task.get('estimated_hours', 1.0)
        importance = task.get('importance', 5) / 10.0
        
        # Quick tasks get highest scores
        base_score = (1.0 / max(effort, 0.1)) * 50
        importance_modifier = 0.3 + 0.7 * importance
        
        return min(base_score * importance_modifier, 100.0)

class HighImpactStrategy(ScoringStrategy):
    """Prioritize high importance tasks regardless of effort"""
    
    def calculate_score(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        importance = task.get('importance', 5)
        effort = task.get('estimated_hours', 1.0)
        
        # Square importance to emphasize high-value tasks
        base_score = (importance ** 2) / 1.5
        # Minimal effort penalty
        effort_penalty = 1.0 / math.log(max(effort, 1) + 1)
        
        return min(base_score * effort_penalty, 100.0)

class DeadlineDrivenStrategy(ScoringStrategy):
    """Prioritize tasks with approaching deadlines"""
    
    def calculate_score(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        due_date = task.get('due_date')
        importance = task.get('importance', 5)
        
        if not due_date:
            return 30.0  # Medium priority for no deadline
        
        now = datetime.now().replace(tzinfo=due_date.tzinfo) if due_date.tzinfo else datetime.now()
        hours_until_due = (due_date - now).total_seconds() / 3600
        
        if hours_until_due <= 0:
            urgency = 100.0  # Past due - maximum urgency
        elif hours_until_due <= 24:
            urgency = 80.0   # Due within 24 hours
        elif hours_until_due <= 72:
            urgency = 60.0   # Due in 3 days
        elif hours_until_due <= 168:
            urgency = 40.0   # Due in 1 week
        else:
            urgency = 20.0   # Not urgent
        
        importance_modifier = 0.5 + (importance / 20.0)  # 0.55 to 1.0
        
        return min(urgency * importance_modifier, 100.0)

class SmartBalanceStrategy(ScoringStrategy):
    """Balanced approach considering all factors with weights"""
    
    def calculate_score(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        importance = task.get('importance', 5)
        effort = task.get('estimated_hours', 1.0)
        due_date = task.get('due_date')
        dependencies = task.get('dependencies', [])
        
        # Weighted components
        importance_score = self._calculate_importance_score(importance)  # 0-40
        urgency_score = self._calculate_urgency_score(due_date)          # 0-35
        effort_score = self._calculate_effort_score(effort)              # 0-15
        dependency_score = self._calculate_dependency_score(task, all_tasks)  # 0-10
        
        total_score = importance_score + urgency_score + effort_score + dependency_score
        
        return min(total_score, 100.0)
    
    def _calculate_importance_score(self, importance: int) -> float:
        """Calculate score based on task importance (0-40 points)"""
        if importance >= 9:
            return 40.0
        elif importance >= 7:
            return 32.0
        elif importance >= 5:
            return 24.0
        elif importance >= 3:
            return 16.0
        else:
            return 8.0
    
    def _calculate_urgency_score(self, due_date) -> float:
        """Calculate score based on urgency (0-35 points)"""
        if not due_date:
            return 10.0
        
        now = datetime.now().replace(tzinfo=due_date.tzinfo) if due_date.tzinfo else datetime.now()
        hours_until_due = (due_date - now).total_seconds() / 3600
        
        if hours_until_due <= 0:
            return 35.0  # Past due
        elif hours_until_due <= 24:
            return 30.0  # Due today
        elif hours_until_due <= 72:
            return 22.0  # Due in 3 days
        elif hours_until_due <= 168:
            return 15.0  # Due in 1 week
        else:
            return 8.0   # Not urgent
    
    def _calculate_effort_score(self, effort: float) -> float:
        """Calculate score based on effort (0-15 points) - inverse relationship"""
        if effort <= 1:
            return 15.0  # Very quick tasks
        elif effort <= 4:
            return 12.0  # Quick tasks
        elif effort <= 8:
            return 8.0   # Medium effort
        elif effort <= 16:
            return 5.0   # High effort
        else:
            return 3.0   # Very high effort
    
    def _calculate_dependency_score(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        """Calculate score based on dependency impact (0-10 points)"""
        task_id = task.get('id')
        if not task_id:
            return 3.0
        
        # Count how many tasks depend on this one
        dependent_count = 0
        for other_task in all_tasks:
            if task_id in other_task.get('dependencies', []):
                dependent_count += 1
        
        if dependent_count >= 3:
            return 10.0
        elif dependent_count == 2:
            return 7.0
        elif dependent_count == 1:
            return 4.0
        else:
            return 1.0

class StrategyFactory:
    """Factory class to create scoring strategies"""
    
    @staticmethod
    def create_strategy(strategy_name: str) -> ScoringStrategy:
        strategies = {
            'fastest_wins': FastestWinsStrategy,
            'high_impact': HighImpactStrategy,
            'deadline_driven': DeadlineDrivenStrategy,
            'smart_balance': SmartBalanceStrategy,
        }
        
        strategy_class = strategies.get(strategy_name, SmartBalanceStrategy)
        return strategy_class()