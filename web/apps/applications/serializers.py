from rest_framework import serializers
from .models import Application, ApplicationNote, StatusChange

class ApplicationNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationNote
        fields = ['id', 'application', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']

class StatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusChange
        fields = ['id', 'from_status', 'to_status', 'changed_at']
        read_only_fields = ['id', 'from_status', 'to_status', 'changed_at']

class ApplicationSerializer(serializers.ModelSerializer):
    application_notes = ApplicationNoteSerializer(many=True, read_only=True)
    timeline = StatusChangeSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'company', 'role', 'status', 'location', 'url', 'notes', 
            'applied_at', 'updated_at', 'resume', 'application_notes', 'timeline'
        ]
        read_only_fields = ['id', 'updated_at']

    def create(self, validated_data):
        # Automatically set the user to the requesting user
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
