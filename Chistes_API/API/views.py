from rest_framework import status
import requests
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from API.models import Chistes
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from API.serializers import ChisteSerializer



@api_view(['GET', 'POST', 'PUT', 'DELETE'])

def chistes_Chuck(request, pk):
    if(pk):
        response = requests.get('https://api.chucknorris.io/jokes/random')
        return Response (response.json())
        



class ChistesView(APIView):
    def get (self,request,pk):
        if(pk>0):
            obj = Chistes.objects.filter(pk=pk).values()
            serializer = ChisteSerializer(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else: 
            mensaje = {"joke not found"}
            return Response(mensaje, status=status.HTTP_404_NOT_FOUND)


    def post (self,request,pk):    
        serializer = ChisteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


    def put (seld,request, pk):
        try:
            obj = Chistes.objects.get(pk=pk)
        except Chistes.DoesNotExist:
            mensaje = {"Not found error"}
            return Response(mensaje, status=status.HTTP_404_NOT_FOUND)
        serializer = ChisteSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)           
        


    def delete (self,request,pk):
        try:
            obj = Chistes.objects.get(pk=pk)
        except Chistes.DoesNotExist:
            mensaje = {"Joke not found"}
            return Response(mensaje, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({"Joke delete"}, status=status.HTTP_204_NO_CONTENT)        
      





















 











