from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from main.models import Tournament, Team
from .serializers import TournamentSerializer, TeamSerializer

class TournamentListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the tournament items for given requested user
        '''
        tournament = Tournament.objects.filter(owner = request.user.id)
        serializer = TournamentSerializer(tournament, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Tournament with given tournament data
        '''
        data = {
            'name': request.data.get('name'), 
            'description': request.data.get('description'), 
            'owner': request.data.get('owner'), 
        }
        serializer = TournamentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TournamentDetailApiView(APIView):

    def get_object(self, tournament_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Tournament.objects.get(id=tournament_id, owner = user_id)
        except Tournament.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, tournament_id, *args, **kwargs):
        '''
        Retrieves the Tournament with given todo_id
        '''
        tournament_instance = self.get_object(tournament_id, request.user.id)
        if not tournament_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TournamentSerializer(tournament_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, tournament_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        tournament_instance = self.get_object(tournament_id, request.user.id)
        if not tournament_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'), 
            'description': request.data.get('description'), 
            'owner': request.data.get('owner'), 
        }
        serializer = TournamentSerializer(instance = tournament_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, tournament_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        tournament_instance = self.get_object(tournament_id, request.user.id)
        if not tournament_instance:
            return Response(
                {"res": "Object with tournament_id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        tournament_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )