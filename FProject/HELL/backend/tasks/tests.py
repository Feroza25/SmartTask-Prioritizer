from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Task
from task_analyzer.scoring.algorithms import TaskScorer

class TaskModelTest(TestCase):
    def test_task_creation(self):
        task = Task.objects.create(
            title="Test Task",
            estimated_hours=2.0,
            importance=7
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.estimated_hours, 2.0)
        self.assertEqual(task.importance, 7)
    
    def test_importance_validation(self):
        task = Task(title="Test", importance=11)
        with self.assertRaises(Exception):
            task.full_clean()

class ScoringAlgorithmTest(TestCase):
    def setUp(self):
        self.scorer = TaskScorer()
        self.sample_tasks = [
            {
                'title': 'Urgent Task',
                'due_date': timezone.now() + timedelta(hours=12),
                'estimated_hours': 2.0,
                'importance': 9,
                'dependencies': []
            },
            {
                'title': 'Important Task', 
                'due_date': None,
                'estimated_hours': 4.0,
                'importance': 10,
                'dependencies': []
            }
        ]
    
    def test_smart_balance_strategy(self):
        score = self.scorer.calculate_score(
            self.sample_tasks[0], 
            self.sample_tasks
        )
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_fastest_wins_strategy(self):
        self.scorer.strategy = 'fastest_wins'
        score = self.scorer.calculate_score(
            self.sample_tasks[0],
            self.sample_tasks
        )
        # Quick task should score higher in fastest wins
        self.assertGreater(score, 0)
    
    def test_high_impact