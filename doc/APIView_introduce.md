`APIView`类是对原生django中`View`类的继承, 它是rest_framework中其他视图类的基类。



```python
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

```