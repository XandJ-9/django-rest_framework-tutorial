from django.urls import path
from rest_framework.routers import SimpleRouter
from myapp.system.views import cbv01, fbv,cbv02

router = SimpleRouter()
router.register(prefix='account', viewset=cbv01.AccountViewSet, basename='account')
# router.register(prefix='account', viewset=cbv.AccountGenericViewSet, basename='account')

urlpatterns = [
    path('db', view=fbv.db, name='db'),
    path('', view=fbv.index, name='index'),
    # path('user/', view=cbv00.UserView.as_view(), name='user'),
    # path('user/', view=cbv01.UserAPIView.as_view(), name='user'),
    path('user/', view=cbv01.UserGenericAPIView.as_view(), name='user'),
    # path('account/', view=cbv.AccountViewSet.as_view(actions ={'get':'list'}), name='account'),
    path('comment/', view=cbv02.CommentGenericAPIView.as_view(), name='comment'),
    path('usercomment/', view=cbv02.UserCommentGenericAPIView.as_view(), name='usercomment'),
]

urlpatterns += router.urls