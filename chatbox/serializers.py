from rest_framework import serializers

from account.serializers import UserSerializer

from .models import ChatBotMessage, Chat


class ChatSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'user', 'modified_at_formatted']

class ChatBotMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ChatBotMessage
        fields = ['id', 'user', 'user_input', 'bot_response', 'created_at_formatted']


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = ChatBotMessageSerializer(read_only=True, many=True)
    
    class Meta:
        model = Chat
        fields = ('id', 'user', 'modified_at_formatted', 'messages',)
    
