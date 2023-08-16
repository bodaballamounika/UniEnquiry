from django.http import JsonResponse

from rest_framework.decorators import authentication_classes, api_view, permission_classes

from .forms import SignupForm

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    """Endpoint to handle the sign up process."""
    data = request.data
    message = 'success'
    
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),

    })
    
    if form.is_valid():
        form.save()
        
        # Send verification email later!
    else:
        message = 'error'
    
    return JsonResponse({'message': message})


@api_view(['GET'])
def me(request):
    """Endpoint to handle the login process."""
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })
