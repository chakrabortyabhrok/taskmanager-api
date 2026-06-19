from rest_framework import serializers
from .models import Task, Category

class TaskSerializer(serializers.ModelSerializer):
    category = serializers.CharField(
        write_only=True, 
        required=False, 
        allow_null=True
    )

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
        ]

    def create(self, validated_data):
        category_name = validated_data.pop('category', None)

        if category_name:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower().replace(" ", "-")}
            )
            validated_data['category'] = category

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.category:
            representation['category'] = instance.category.name
        else:
            representation['category'] = None
        return representation
    
