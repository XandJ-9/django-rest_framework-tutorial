from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drones.models import DroneCategory, Drone, Pilot, Competition
from drones.serializers import DroneCategorySerializer, DroneSerializer, PilotSerializer, PilotCompetitionSerializer
from drones.custompermission import IsCurrentUserOwnerOrReadOnly

# Create your views here.

# class ApiRoot(generics.GenericAPIView):
#     name = 'api-root'
#     def get(self, request):
#         return Response({
#             "categories/": reverse(DroneCategoryViewSet.name),
#             "drones/": reverse(DroneList.name),
#             "pilots/": reverse(PilotList.name),
#             "competitions/": reverse(CompetitionList.name),
#         })


# class DroneCategoryList(generics.ListCreateAPIView):
#     queryset = DroneCategory.objects.all()
#     serializer_class = DroneCategorySerializer
#     name = 'dronecategory-list'



# class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = DroneCategory.objects.all()
#     serializer_class = DroneCategorySerializer
#     name = 'dronecategory-detail'


class DroneCategoryViewSet(ModelViewSet):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer


# class DroneList(generics.ListCreateAPIView):
#     queryset = Drone.objects.all()
#     serializer_class = DroneSerializer
#     name = 'drone-list'


# class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Drone.objects.all()
#     serializer_class = DroneSerializer
#     name = 'drone-detail'

class DroneViewSet(ModelViewSet):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCurrentUserOwnerOrReadOnly]
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

# class PilotList(generics.ListCreateAPIView):
#     queryset = Pilot.objects.all()
#     serializer_class = PilotSerializer
#     name = 'pilot-list'


# class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Pilot.objects.all()
#     serializer_class = PilotSerializer
#     name = 'pilot-detail'

class PilotViewSet(ModelViewSet):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer

# class CompetitionList(generics.ListCreateAPIView):
#     queryset = Competition.objects.all()
#     serializer_class = PilotCompetitionSerializer
#     name = 'competition-list'


# class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Competition.objects.all()
#     serializer_class = PilotCompetitionSerializer
#     name = 'competition-detail'


class CompetitionViewSet(ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
