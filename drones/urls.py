from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter, APIRootView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

# from .views import ApiRoot, DroneCategoryList,DroneCategoryDetail,DroneList, DroneDetail, CompetitionList, CompetitionDetail, PilotList, PilotDetail
from .views import DroneCategoryViewSet, PilotViewSet, DroneViewSet, CompetitionViewSet

router = DefaultRouter()
router.register(r'dronecategory', DroneCategoryViewSet, basename='dronecategory')
router.register(r'drone', DroneViewSet, basename='drone')
router.register(r'pilot', PilotViewSet, basename='pilot')
router.register(r'competition', CompetitionViewSet, basename='competition')


urlpatterns = [
    path('', router.get_api_root_view()), 
    # path('categories/', DroneCategoryList.as_view(), name=DroneCategoryList.name),
    # path('category/<int:pk>', DroneCategoryDetail.as_view(), name=DroneCategoryDetail.name),
    # path('drones/', DroneList.as_view(), name=DroneList.name),
    # path('drone/<int:pk>', DroneDetail.as_view(), name=DroneDetail.name),
    # path('pilots/', PilotList.as_view(), name=PilotList.name),
    # path('pilot/<int:pk>', PilotDetail.as_view(), name=PilotDetail.name),
    # path('competitions/', CompetitionList.as_view(), name=CompetitionList.name),
    # path('competition/<int:pk>', CompetitionDetail.as_view(), name=CompetitionDetail.name),
]




urlpatterns += router.urls