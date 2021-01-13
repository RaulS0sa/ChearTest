from rest_framework import serializers
from django.db import models
from math import radians, cos, sin, asin, sqrt
from app.models import UserForm

class Location(object):
    def __init__(self, lat, longitude):
        self.Latidude = lat
        self.Longitude = longitude

class DistancePair(object):
    def __init__(self, Loc1 , Loc2):
        self.Location1=Loc1
        self.Location2 = Loc2

class LocationSerializer(serializers.Serializer):
    Latitude = serializers.FloatField(max_value=90, min_value=-90)
    Longitude = serializers.FloatField(max_value=180, min_value=-180)

    def create(self, validated_data):
        return Location(**validated_data)

class DistancePairSerializer(serializers.Serializer):
    Location1=LocationSerializer()
    Location2=LocationSerializer()

    def create(self, validated_data):
         Location1 = self.validated_data.pop('Location1')
         Location2 = self.validated_data.pop('Location2')
         
         return DistancePair(Location1,Location2)
    def haversine(self):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1 = self.data["Location1"]["Longitude"]
        lat1 = self.data["Location1"]["Latitude"]
        lon2 = self.data["Location2"]["Longitude"]
        lat2 = self.data["Location2"]["Latitude"]
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

class ListObject(object):
    def __init__(self, List):
        self.WordList=List
        
class WordListSerializer(serializers.Serializer):
   WordList = serializers.ListField(child=serializers.CharField(), min_length=10, max_length=10)
   def create(self, validated_data):
       return ListObject(**validated_data)
   def MatchingWords(self):
       SetOfWords = set(self.data["WordList"])
       ReturnDict = dict()
       for element in SetOfWords:
           ReturnDict[element] = self.data["WordList"].count(element)
       return ReturnDict

class IDObject(object):
    def __init__(self, ID):
        self.id=ID
class IDSerializer(serializers.Serializer):
    id = serializers.IntegerField(max_value=None, min_value=0)
    def create(self, validated_data):
        return IDObject(**validated_data)

class UserObject(object):
    def __init__(self, name,passw):
        self.username=name
        self.password=passw
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def create(self, validated_data):
        return UserObject(**validated_data)
class UpdateUserObject(object):
    def __init__(self,ID, name,passw):
        self.username=name
        self.password=passw
        self.id=ID
class UpdateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    id = serializers.IntegerField(max_value=None, min_value=0)
    def create(self, validated_data):
        return UpdateUserObject(**validated_data)


