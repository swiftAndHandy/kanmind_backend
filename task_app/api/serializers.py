from rest_framework import serializers

from auth_app.api.serializers import UserProfileSerializer
from auth_app.models import UserProfile
from task_app.models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task list and create endpoints.
    assignee and reviewer are nested response objects (read_only),
    but accepted as IDs (assignee_id, reviewer_id) in request.
    Both are optional and nullable; a task can exist without either.
    """
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),
                                                     write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),
                                                     write_only=True, required=False, allow_null=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'assignee', 'reviewer_id',
                  'reviewer', 'due_date', 'comments_count']

    def create(self, validated_data):
        # must popped and set separately because they don't directly map to the model field names
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
    """
    Required for Task PATCH endpoint.
    Identical to TaskSerializer except for the board field. Board can't be changed after creation.
    assignee and reviewer are only updated if explicitly included inside request,
    allowing them to become null without affecting omitted fields.
    """
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),
                                                     write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(),
                                                     write_only=True, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assignee_id', 'assignee', 'reviewer_id',
                  'reviewer', 'due_date']

    def update(self, instance, validated_data):
        # assignee_id and reviewer_id are only updated if explicitly included in the request.
        # Using 'in validated_data' instead of pop(..., None) distinguishes between:
        # - field omitted entirely -> key not present -> existing value preserved
        # - field explicitly set to null -> key present with None value -> assignment removed
        # This allows intentional removal of assignee/reviewer without affecting omitted fields.
        if 'assignee_id' in validated_data:
            instance.assignee = validated_data.pop('assignee_id')

        if 'reviewer_id' in validated_data:
            instance.reviewer = validated_data.pop('reviewer_id')

        instance = super().update(instance, validated_data)
        return instance

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment list and create endpoints.
    author  uses source= to return only the fullname string instead of UserProfile,
    as required by the API response format.
    craeted_at is set automatically when a comment is created via auto_now_add=True and cannot be overridden.
    """
    author = serializers.CharField(source='author.fullname', read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'author', 'content')