from rest_framework import serializers
from .models import Task, Category
from core.ai_utils import generate_task_summary, add_task_to_vectorstore

class TaskSerializer(serializers.ModelSerializer):
    """ Serializer for Task model with custom category handling and AI summary. """
    category = serializers.CharField(
        write_only=True, 
        required=False, 
        allow_null=True
    )

    #ai_summary = serializers.CharField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'category',
            'due_date',
            'created_at',
            'updated_at',
            'ai_summary'
        ]
    
    def create(self, validated_data):
        category_name = validated_data.pop('category', None)

        if category_name:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower().replace(" ", "-")}
            )
            validated_data['category'] = category

        # Just create the task normally (no AI, no Chroma for now)
        task = super().create(validated_data)
        return task
    
    def update(self, instance, validated_data):
        """Handle category update + regenerate AI summary after task is updated."""
        category_name = validated_data.pop('category', None)

        if category_name:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower().replace(" ", "-")}
            )
            validated_data['category'] = category

        """ Update the task """
        task = super().update(instance, validated_data)

        """ Regenerate summary after update """
        try:
            task.ai_summary = generate_task_summary(task)
            task.save(update_fields=['ai_summary'])
            add_task_to_vectorstore(task)

        except Exception as e:
            print(f"AI Summary failed for task {task.id}: {e}")
            
        # task.ai_summary = generate_task_summary(task)
        # task.save(update_fields=['ai_summary'])

        return task

    def to_representation(self, instance):
        """Show category name instead of ID in response."""
        representation = super().to_representation(instance)
        if instance.category:
            representation['category'] = instance.category.name
        else:
            representation['category'] = None
        return representation