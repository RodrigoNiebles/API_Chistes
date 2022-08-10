from rest_framework import status
import requests
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from API.models import Chistes
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from API.serializers import ChisteSerializer
#from Chistes_API.API import serializers
#from Chistes_API.API import serializers


@api_view(['GET', 'POST', 'PUT', 'DELETE'])

def chistes_list(request, pk):
    if(id):
        r = requests.get('https://api.chucknorris.io/jokes/random')
        return HttpResponse(r)


class ChistesView(APIView):
    def get (self,request):
        obj = Chistes.objects.all()
        serializer = ChisteSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post (self,request):    
        serializer = ChisteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  










    '''try:
        chistes = Chistes.objects.get(pk=pk)
    except Chistes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    


    if request.method == 'GET':
        response = requests.get ('https://api.chucknorris.io/jokes/random')
        print('rodri'+response)'''
        











        #serializer = ChisteSerializer(chistes)
        #return Response(serializer.data)

    '''elif request.method == 'PUT':
        serializer = ChisteSerializer(chistes, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        chistes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) '''   





#def get(self,request):
 #   response= requests.get ('https://api.chucknorris.io/jokes/random')
       
  #  print(response)
       #serializer = ChisteSerializer
       #return Response(serializer.data)





