from django.urls import path
from rest_framework.routers import SimpleRouter
from myapp.system.views import fbv,cbv, cbv_00

router = SimpleRouter()
router.register(prefix='account', viewset=cbv.AccountViewSet, basename='account')
# router.register(prefix='account', viewset=cbv.AccountGenericViewSet, basename='account')

urlpatterns = [
    path('db', view=fbv.db, name='db'),
    path('', view=fbv.index, name='index'),
    # path('user/', view=cbv_00.UserView.as_view(), name='user'),
    path('user/', view=cbv.UserAPIView.as_view(), name='user'),
    path('user/', view=cbv.UserGenericAPIView.as_view(), name='user'),
    # path('account/', view=cbv.AccountViewSet.as_view(actions ={'get':'list'}), name='account'),
]

urlpatterns += router.urls