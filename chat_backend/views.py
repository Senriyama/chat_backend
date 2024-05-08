from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import Message
import json

def index(request):
    return render(request, 'index.html')

@require_http_methods(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # デバッグ用
        # print("Username:", username)
        # print("Password:", password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'username': username})
        else:
            return JsonResponse({'status': 'error', 'message': 'Login failed'})
    
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'An error occurred'}, status=500)
    
@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})

@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    # email = request.POST.get('email', '')  # メールはオプションで受け取る
    print(json.dumps({'username': username, 'password': password}))

    if not username or not password:
        return JsonResponse({'status': 'error', 'message': 'Username or password cannot be empty'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'message': 'Username already exists'}, status=400)

    User.objects.create(
        username=username,
        # email=email,
        password=make_password(password))
    return JsonResponse({'status': 'success', 'message': 'User registered successfully'}, status=201)

@csrf_exempt
@require_http_methods(['POST'])
def check_username(request):
    data = json.loads(request.body)
    username = data.get('username')
    if username and User.objects.filter(username=username).exists():
        return JsonResponse({'isValid': False, 'message': 'This username is already taken'}, status=400)
    return JsonResponse({'isValid': True})

@csrf_exempt
@login_required
@require_http_methods(['GET', 'POST'])
def message_view(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            message = data.get('message')
            if not message:
                return JsonResponse({'status': 'error', 'message': 'Message is required.'}, status=400)

            Message.objects.create(user=request.user, text=message)
            return JsonResponse({'status': 'success', 'message': 'Message saved'}, status=201)
        
        elif request.method == 'GET':
            messages = Message.objects.all().order_by('-id').values('id', 'user__username', 'text', 'created_at')
            return JsonResponse(list(messages), safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)