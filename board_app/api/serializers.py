from rest_framework import serializers

from auth_app.models import UserProfile
from board_app.models import Board


class BoardSerializer(serializers.ModelSerializer):
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all(), write_only=True)

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'owner_id',
            'members', 'member_count',
            'ticket_count', 'tasks_to_do_count',
            'tasks_high_prio_count',
        ]

    def get_ticket_count(self, obj):
        return 0

    def get_tasks_to_do_count(self, obj):
        return 0

    def get_tasks_high_prio_count(self, obj):
        return 0

    def get_member_count(self, obj):
        return obj.members.count()

    def create(self, validated_data):
        validated_members = validated_data.pop('members')
        instance = super(BoardSerializer, self).create(validated_data)
        instance.members.set(validated_members)
        return instance

