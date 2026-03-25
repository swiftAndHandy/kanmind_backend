from auth_app.api.serializers import UserProfileSerializer
from task_app.models import Task
from rest_framework import serializers
from auth_app.models import UserProfile


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),
                                                     write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),
                                                     write_only=True, required=False, allow_null=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'assignee', 'reviewer_id',
                  'reviewer', 'due_date', 'comments_count')

    def create(self, validated_data):
        assignee = validated_data.pop('assignee_id', None)
        reviewer = validated_data.pop('reviewer_id', None)
        instance = super(TaskSerializer, self).create(validated_data)
        instance.assignee = assignee
        instance.reviewer = reviewer
        instance.save()
        return instance

    def get_comments_count(self, obj):
        return obj.comments.count()

class TaskUpdateSerializer(serializers.ModelSerializer):
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),
                                                     write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),
                                                     write_only=True, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'priority', 'assignee_id', 'assignee', 'reviewer_id',
                  'reviewer', 'due_date')

    def update(self, instance, validated_data):
        if 'assignee_id' in validated_data:
            instance.assignee = validated_data.pop('assignee_id')

        if 'reviewer_id' in validated_data:
            instance.reviewer = validated_data.pop('reviewer_id')

        instance = super().update(instance, validated_data)
        return instance