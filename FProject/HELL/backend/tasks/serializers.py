from rest_framework import serializers
from .models import Task
from datetime import datetime

class TaskSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(read_only=True)
    explanation = serializers.CharField(read_only=True)
    dependencies = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Task.objects.all(), 
        required=False
    )
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'due_date', 'estimated_hours', 
            'importance', 'dependencies', 'score', 'explanation', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_importance(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Importance must be between 1 and 10")
        return value
    
    def validate_estimated_hours(self, value):
        if value <= 0:
            raise serializers.ValidationError("Estimated hours must be positive")
        return value
    
    def validate_due_date(self, value):
        if value and value < datetime.now().replace(tzinfo=value.tzinfo):
            raise serializers.ValidationError("Due date cannot be in the past")
        return value

class TaskAnalyzeSerializer(serializers.Serializer):
    tasks = TaskSerializer(many=True)
    strategy = serializers.ChoiceField(
        choices=Task.SCORING_STRATEGIES, 
        default='smart_balance'
    )
    
    def validate_tasks(self, value):
        if not value:
            raise serializers.ValidationError("At least one task is required")
        return value

class SuggestionSerializer(serializers.Serializer):
    title = serializers.CharField()
    score = serializers.FloatField()
    explanation = serializers.CharField()
    priority = serializers.CharField()