from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

@api_view(['POST'])
def analyze_tasks(request):
    try:
        tasks = request.data.get('tasks', [])
        strategy = request.data.get('strategy', 'smart_balance')
        
        scored_tasks = []
        for task in tasks:
            score = calculate_score(task, strategy)
            explanation = get_explanation(task, score, strategy)
            
            scored_task = {
                **task,
                'score': round(score, 2),
                'explanation': explanation
            }
            scored_tasks.append(scored_task)
        
        scored_tasks.sort(key=lambda x: x['score'], reverse=True)
        
        return Response({
            'tasks': scored_tasks,
            'strategy': strategy,
            'message': f'Analyzed {len(scored_tasks)} tasks'
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def suggest_tasks(request):
    strategy = request.GET.get('strategy', 'smart_balance')
    
    sample_tasks = [
        {
            'title': 'Fix critical bug',
            'due_date': (timezone.now() + timedelta(hours=12)).isoformat(),
            'estimated_hours': 2,
            'importance': 9
        },
        {
            'title': 'Complete project',
            'due_date': (timezone.now() + timedelta(days=2)).isoformat(),
            'estimated_hours': 4,
            'importance': 8
        },
        {
            'title': 'Write documentation',
            'due_date': (timezone.now() + timedelta(days=7)).isoformat(),
            'estimated_hours': 3,
            'importance': 6
        }
    ]
    
    suggestions = []
    for task in sample_tasks:
        score = calculate_score(task, strategy)
        explanation = get_explanation(task, score, strategy)
        priority = 'critical' if score > 80 else 'high' if score > 60 else 'medium'
        
        suggestions.append({
            'title': task['title'],
            'score': round(score, 2),
            'explanation': explanation,
            'priority': priority
        })
    
    suggestions.sort(key=lambda x: x['score'], reverse=True)
    
    return Response({
        'suggestions': suggestions[:3],
        'strategy': strategy
    })

def calculate_score(task, strategy):
    importance = task.get('importance', 5)
    hours = task.get('estimated_hours', 1)
    
    if strategy == 'fastest_wins':
        return min(100, (1 / max(hours, 0.1)) * 20)
    elif strategy == 'high_impact':
        return min(100, importance * 10)
    elif strategy == 'deadline_driven':
        return min(100, importance * 8 + 20)
    else:  # smart_balance
        return min(100, importance * 7 + (1 / max(hours, 0.1)) * 3)

def get_explanation(task, score, strategy):
    importance = task.get('importance', 5)
    hours = task.get('estimated_hours', 1)
    
    strategies = {
        'fastest_wins': 'Quick wins strategy',
        'high_impact': 'High impact focus', 
        'deadline_driven': 'Deadline driven',
        'smart_balance': 'Smart balanced approach'
    }
    
    return f"{strategies[strategy]}: Importance {importance}/10, Effort {hours}h"