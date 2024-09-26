## `ViewSet`

定义：

```python
class ViewSet(ViewSetMixin, views.APIView):
    """
    The base ViewSet class does not provide any actions by default.
    """
    pass
```



ViewSet类是在APIView类的基础上混入了一些行为，在APIView中只有get, post,put,delete等方法是绑定到对应的http请求上的，这样每次处理一类对象的操作都需要单独为其写一个视图类，使用ViewSet可以避免这些操作（当然如果是采用f函数视图的方式也可以），ViewSet结合`@actions`注解可以绑定不同的方法。

ViewSet有两种使用方式，一种是直接调用`as_view()`方法，但是需要提供参数actions，例如：

`path('account/', view=cbv.AccountViewSet.as_view(actions ={'get':'list'}), name='account')`

另一种则是结合路由对象来使用，例如：

```python
from django.urls import path
from rest_framework.routers import SimpleRouter
from myapp.system.views import fbv,cbv, cbv_00

router = SimpleRouter()
router.register(prefix='account', viewset=cbv.AccountViewSet, basename='account')

urlpatterns = [
    # path('account/', view=cbv.AccountViewSet.as_view(actions ={'get':'list'}), name='account'),
]

urlpatterns += router.urls
```

使用路由方式的优点是可以更加灵活的自定义请求处理方法，只需要通过`@actions`注解

```python
class AccountViewSet(ViewSet):
    '''
    继承ViewSet，实现增删改查
    viewset没有提供任何的行为来处理请求，因此需要提供一个actions参数来指定处理函数
    1. AccountViewSet.as_view(actions ={'get':'list',...})
        需要实现 list, create, retrieve, update, destroy等方法
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
    
    @action(methods=['get'], detail=False, url_path="get_list")
    def get_list(self, request):
        account_list = Account.objects.all()
        ser = AccountSerializer(account_list, many=True)
        return Response({"msg":"get_list请求", "list":ser.data})

```