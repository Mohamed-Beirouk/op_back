from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Categorie, ObjectPerdus
from op_app.serializer import CategorieSerializer, ObjectPerdusSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):    
    data = request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already exists'}, status=400)
    if not all([first_name, last_name, email, password, username]):
        return JsonResponse({'error': 'All fields are required'}, status=400)
    user = User.objects.create_user(
        email=email,
        
        first_name=first_name,
        last_name=last_name,
        username=username
    )
    user.save()
    user.set_password(password)
    user.save()
    serializer = UserSerializer(user, many=False)
    return JsonResponse(serializer.data, status=201)



# catgeories
@api_view(['GET'])
@permission_classes([AllowAny])
def list_categories(request):
    categories = Categorie.objects.all()
    serializer = CategorieSerializer(categories, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_objects_perdus(request):
    ops = ObjectPerdus.objects.filter(status='found').order_by('-date_found')
    serializer = ObjectPerdusSerializer(ops, many=True)
    return JsonResponse(serializer.data, safe=False)



from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_object_perdus(request):
    print(request.user)
    # print(request.FILES)
    print(request.data)
    data = request.data
    title = data.get('title')
    description = data.get('description')
    date_found = data.get('date_found')
    location_found = data.get('location_found')
    category_id = data.get('category')
    found_by = request.user
    image = request.FILES.get('image')

    if not all([title, description, date_found, location_found, category_id]):
        return JsonResponse({'error': 'All fields are required'}, status=400)

    try:
        category = Categorie.objects.get(id=category_id)
    except Categorie.DoesNotExist:
        return JsonResponse({'error': 'Invalid category'}, status=400)

    op = ObjectPerdus.objects.create(
        title=title,
        description=description,
        date_found=date_found,
        location_found=location_found,
        category=category,
        found_by=found_by
    )
    if image:
        op.image = image
        op.save()
    serializer = ObjectPerdusSerializer(op, many=False)
    return JsonResponse(serializer.data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def return_object_perdus(request, op_id):
    try:
        op = ObjectPerdus.objects.get(id=op_id)
    except ObjectPerdus.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    if op.status == 'returned':
        return JsonResponse({'error': 'Already returned'}, status=400)
    op.status = 'returned'
    op.save()
    serializer = ObjectPerdusSerializer(op, many=False)
    return JsonResponse(serializer.data, status=200)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_objects_perdus(request):
    ops = ObjectPerdus.objects.filter(found_by=request.user).order_by('status','-date_found')
    serializer = ObjectPerdusSerializer(ops, many=True)
    return JsonResponse(serializer.data, safe=False)