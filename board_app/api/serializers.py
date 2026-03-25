from rest_framework import serializers

from auth_app.api.serializers import UserProfileSerializer
from auth_app.models import UserProfile
from board_app.models import Board
from task_app.api.serializers import TaskSerializer


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for Board list and create endpoints.
    Counts are calculated via SerializerMethodField because they
    are derived from related models (Task, Members) and not stored in Database.
    members is_write only: accepted on POST but never returned in response.
    """
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all(), write_only=True)

    class Meta:
        model = Board
        fields = [
            'id', 'title',
            'members', 'member_count',
            'ticket_count', 'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id',
        ]

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()

    def get_member_count(self, obj):
        return obj.members.count()

    def create(self, validated_data):
        # pop members -> many to many MUST be set AFTER instance initializing.
        validated_members = validated_data.pop('members')
        instance = super(BoardSerializer, self).create(validated_data)
        instance.members.set(validated_members)
        return instance


class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserProfileSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'owner_id', 'members', 'tasks'
        ]

class BoardUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Board PATCH endpoint.
    owner_data and members_data use source= because the fields differ from model field names.
    member is write_only: IDs come in, nested objects go out via member_data.
    """
    members = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=UserProfile.objects.all())

    owner_data = UserProfileSerializer(source='owner', read_only=True)
    members_data = UserProfileSerializer(source='members', many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members', 'members_data']

    def update(self, instance, validated_data):
        # .get() with fallback to preserve existing values for omitted fields (PATCH behavior)
        instance.title = validated_data.get('title', instance.title)
        instance.members.set(validated_data.get('members', instance.members.all()))
        instance.save()
        return instance

