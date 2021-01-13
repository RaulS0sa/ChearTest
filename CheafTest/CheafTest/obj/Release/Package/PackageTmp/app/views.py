"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from rest_framework.parsers import JSONParser
#from Serializers.Serializers import DistancePairSerializer

from django.views.decorators.csrf import csrf_exempt

from app.Serializers.Serializers import DistancePairSerializer
from app.Serializers.Serializers import WordListSerializer
from app.Serializers.Serializers import UserSerializer
from app.Serializers.Serializers import IDSerializer
from app.Serializers.Serializers import UpdateSerializer
from app.models import UserForm



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
@csrf_exempt
def DistanceCalculation(request):
    """
    Calculate Distance acording to haversine formula
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DistancePairSerializer(data=data)
        if serializer.is_valid():
            ReturnData = dict()
            ReturnData["DistanceKM"] = serializer.haversine()
            return JsonResponse(ReturnData, status=200)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse("The API verb is incorrect or any other error has happen", status=404)

@csrf_exempt
def WordListing(request):
    """
    Counts each distinct word in array
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = WordListSerializer(data=data)
        if serializer.is_valid():
            ReturnData = dict()
            ReturnData["WordsArray"] = serializer.MatchingWords()
            return JsonResponse(ReturnData, status=200)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse("The API verb is incorrect or any other error has happen", status=404)

@csrf_exempt
def CreateUser(request):
    """
    creates user
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            
            user_name = serializer.data["username"]
            user_password = serializer.data["password"]
            us = UserForm(username=user_name,password=user_password)
            us.save()
            ReturnData = dict()
            ReturnData["ID"] = us.id
            return JsonResponse(ReturnData, status=200)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse("The API verb is incorrect or any other error has happen", status=404)

@csrf_exempt
def ReadUser(request):
    """
    returns username according to id
    """
    if request.method == 'GET':
        ReturnData = dict()
        try:
            
            user_id = request.GET.get('user_id', None)
            user = UserForm.objects.get(pk=user_id)
            ReturnData["Username"] = user.username
            return JsonResponse(ReturnData, status=200)
        except:
            ReturnData["error"] = "No valid user"
            return JsonResponse(ReturnData, status=404)
        return JsonResponse(serializer.errors, status=400)
    ReturnData["error"] = "internal server errorr"
    return JsonResponse(ReturnData, status=500)

@csrf_exempt
def UpdateUser(request):
    """
    Updates Username and password according to id
    """
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UpdateSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserForm.objects.get(pk=user_id)
            user.username = serializer.data["username"]
            user.password = serializer.data["password"]
            user.save()
            ReturnData = dict()
            ReturnData["Response"] = "updated"
            return JsonResponse(ReturnData, status=200)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse("The API verb is incorrect or any other error has happen", status=404)

@csrf_exempt
def DestroyUser(request):
    """
    Delete User
    """
    if request.method == 'DELETE':
        data = JSONParser().parse(request)
        serializer = IDSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            user = UserForm.objects.get(pk=user_id)
            user.delete()
            ReturnData = dict()
            ReturnData["Response"] = "Destroyed"
            return JsonResponse(ReturnData, status=200)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse("The API verb is incorrect or any other error has happen", status=404)

