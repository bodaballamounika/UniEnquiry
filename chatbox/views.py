from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, api_view, permission_classes

from chatbox.chat import get_response

from .models import Chat, ChatBotMessage
from .serializers import ChatBotMessageSerializer, ChatSerializer, ChatDetailSerializer


@api_view(['POST'])
def chatbot(request):
    # chat = Chat.objects.get(user=user, pk=pk)
    data = request.data
    
    print(data)
    user_input = data.get('userInput', '').strip()
    
    if user_input:
        response = get_response(user_input)
        # chat_message = ChatBotMessage.objects.create(
        #     chat=chat,
        #     user_input=user_input,
        #     bot_response=response,
        #     user=request.user
        # )
        # serializer = ChatBotMessageSerializer(chat_message)
        
        
        return JsonResponse({'response': response})
    
    return JsonResponse({})


@api_view(['GET'])
def chat_list(request):
    chats = Chat.objects.filter(user=request.user)
    serializer = ChatSerializer(chats, many=True)
    
    
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def chat_detail(request, pk):
    chat = Chat.objects.get(user=request.user, pk=pk)
    serializer = ChatDetailSerializer(chat)
    
    print(serializer.data)
    
    return JsonResponse(serializer.data, safe=False)
