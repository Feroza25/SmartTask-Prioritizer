from datetime import datetime, timedelta
from typing import List, Dict, Any
import math

class TaskScorer:
    def __init__(self, strategy='smart_balance'):
        self.strategy = strategy
    
    def calculate_score(self, task_data: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        """Calculate priority score based on selected strategy"""
        
        if self.strategy == 'fastest_wins':
            return self._fastest_wins_strategy(task_data)
        elif self.strategy == 'high_impact':
            return self._high_impact_strategy(task_data)
        elif self.strategy == 'deadline_driven':
            return self._deadline_driven_strategy(task_data)
        else:  # smart_balance
            return self._smart_balance_strategy(task_data, all_tasks)
    
    def _fastest_wins_strategy(self, task: Dict[str, Any]) -> float:
        """Prioritize quick wins - lower effort = higher priority"""
        effort = task.get('estimated_hours', 1.0)
        importance = task.get('importance', 5) / 10.0
        
        # Inverse of effort with importance modifier
        base_score = (1.0 / max(effort, 0.1)) * 10
        return base_score * (0.3 + 0.7 * importance)
    
    def _high_impact_strategy(self, task: Dict[str, Any]) -> float:
        """Prioritize high importance tasks"""
        importance = task.get('importance', 5)
        effort = task.get('estimated_hours', 1.0)
        
        # Square importance to emphasize high-value tasks
        base_score = (importance ** 2) / 2.0
        effort_penalty = 1.0 / math.log(max(effort, 1) + 1)
        
        return base_score * effort_penalty
    
    def _deadline_driven_strategy(self, task: Dict[str, Any]) -> float:
        """Prioritize urgent deadlines"""
        due_date = task.get('due_date')
        if not due_date:
            return 5.0  # Default medium priority for no deadline
        
        importance = task.get('importance', 5)
        now = datetime.now().replace(tzinfo=due_date.tzinfo) if due_date.tzinfo else datetime.now()
        time_until_due = (due_date - now).total_seconds() / 3600  # hours
        
        if time_until_due <= 0:
            # Past due - very high priority
            urgency = 100.0
        elif time_until_due <= 24:
            # Due within 24 hours
            urgency = 50.0
        elif time_until_due <= 168:  # 1 week
            urgency = 25.0
        else:
            urgency = 10.0
        
        return urgency * (importance / 10.0)
    
    def _smart_balance_strategy(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        """Balanced approach considering all factors"""
        importance = task.get('importance', 5)
        effort = task.get('estimated_hours', 1.0)
        due_date = task.get('due_date')
        dependencies = task.get('dependencies', [])
        
        # Importance component (0-40 points)
        importance_score = (importance ** 1.5) * 2.0
        
        # Urgency component (0-40 points)
        urgency_score = self._calculate_urgency(due_date)
        
        # Effort component (0-20 points) - inverse relationship
        effort_score = (1.0 / math.log(max(effort, 1) + 1)) * 20
        
        # Dependency weight (0-20 points)
        dependency_score = self._calculate_dependency_weight(task, all_tasks)
        
        total_score = importance_score + urgency_score + effort_score + dependency_score
        
        return min(total_score, 100.0)  # Cap at 100
    
    def _calculate_urgency(self, due_date) -> float:
        if not due_date:
            return 10.0  # Medium priority for no deadline
        
        now = datetime.now().replace(tzinfo=due_date.tzinfo) if due_date.tzinfo else datetime.now()
        hours_until_due = (due_date - now).total_seconds() / 3600
        
        if hours_until_due <= 0:
            return 40.0  # Past due - maximum urgency
        elif hours_until_due <= 24:
            return 35.0  # Due today
        elif hours_until_due <= 72:
            return 25.0  # Due in 3 days
        elif hours_until_due <= 168:
            return 15.0  # Due in 1 week
        else:
            return 5.0   # Not urgent
    
    def _calculate_dependency_weight(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> float:
        """Calculate score based on how many tasks depend on this one"""
        task_id = task.get('id')
        if not task_id:
            return 5.0
        
        # Count how many tasks have this task as a dependency
        dependent_count = 0
        for other_task in all_tasks:
            if task_id in other_task.get('dependencies', []):
                dependent_count += 1
        
        # More dependents = higher priority
        return min(dependent_count * 3.0, 20.0)