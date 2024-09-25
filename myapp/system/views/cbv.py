from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action

from myapp.system.models import User, Account

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']

class UserAPIView(APIView):
    '''
    继承APIView，实现增删改查
    需要实现get,post,delete,put等方法
    '''
    def get(self,request):
        # 使用原生查询，从另外的库中查询数据返回
        user_list = User.objects.raw("select id,username, password from sys_user")
        # user_list = User.objects.all()
        ser = UserSerializer(user_list,many=True)
        return Response({"msg":"get请求", "list":ser.data})
    def post(self,request):
        ser = UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"msg":"保存对象"})
        else:
            return Response({"msg":"数据不合法"})

    def put(self,request):
        return Response({"msg":"put请求"})

    def delete(self,request):
        return Response({"msg":"delete请求"})

class UserGenericAPIView(GenericAPIView):
    '''
    继承GenericAPIView，实现增删改查
    GenericAPIView类将提供了获取对象集queryset和序列化器serializer_class的默认实现
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self,request):
        ser = self.get_serializer(instance=self.get_queryset(), many = True)
        return Response({"msg":"get请求", "data":ser.data})

class AccountViewSet(ViewSet):
    '''
    继承ViewSet，实现增删改查
    viewset没有提供任何的行为来处理请求，因此需要提供一个actions参数来指定处理函数
    1. AccountViewSet.as_view(actions ={'get':'list',...})
    2. 通过注解的方式绑定请求的处理方法 @actions
        @action(methods=['get'],detail=False)
        使用注解时，需要使用Router的方式注册viewset 
      例如：
      router = SimpleRouter()
      router.register(prefix='account', viewset=cbv.AccountViewSet, basename='account')

      urlpatterns = [
          path('db', view=fbv.db, name='db'),
          path('', view=fbv.index, name='index'),
          path('user/', view=cbv.UserView.as_view(), name='user'),
          path('account/', view=cbv.AccountViewSet.as_view(actions ={'get':'list'}), name='account'),
      ]

      urlpatterns += router.urls
    '''

    def list(self,request):
        account_list = Account.objects.all()
        return Response({"msg":"list请求", "list":account_list})
    
    @action(methods=['get'], detail=False, url_path="get_list")
    def get_list(self, request):
        account_list = Account.objects.all()
        return Response({"msg":"get_list请求", "list":account_list})
    
