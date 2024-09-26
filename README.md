# View API



<a href='./doc/APIView_introduce.md'>APIView</a>









## `GenericAPIView`

`GenericAPIView`类继承自`APIView`,可以在这个类中指定对象集和序列化器，甚至可以提供一个获取分页结果集的方法，当然这些方法都是可以在自类中重写，达到满足自定义的需求。

```python
class GenericAPIView(views.APIView):
    """
    Base class for all other generic views.
    """
    # You'll need to either set these attributes,
    # or override `get_queryset()`/`get_serializer_class()`.
    # If you are overriding a view method, it is important that you call
    # `get_queryset()` instead of accessing the `queryset` property directly,
    # as `queryset` will get evaluated only once, and those results are cached
    # for all subsequent requests.
    queryset = None
    serializer_class = None

    # If you want to use object lookups other than pk, set 'lookup_field'.
    # For more complex lookup requirements override `get_object()`.
    lookup_field = 'pk'
    lookup_url_kwarg = None

    # The filter backend classes to use for queryset filtering
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    # The style to use for queryset pagination.
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    # Allow generic typing checking for generic views.
    def __class_getitem__(cls, *args, **kwargs):
        return cls

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def filter_queryset(self, queryset):
        """
        Given a queryset, filter it with whichever filter backend is in use.

        You are unlikely to want to override this method, although you may need
        to call it either from a list view, or from a custom `get_object`
        method if you want to apply the configured filtering backend to the
        default queryset.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
```



自定义子类使用样例

```python
class UserGenericAPIView(GenericAPIView):
    '''
    继承GenericAPIView，实现增删改查
    GenericAPIView类将提供了获取对象集queryset和序列化器serializer_class的默认实现
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self,request):
        ser = self.get_serializer(instance=self.get_queryset(), many = True)
        return Response({"msg":"UserGenericAPIView get请求", "data":ser.data})
```



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



## `GenericViewSet`

定义：

```python
class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass
```

对比ViewSet的定义可以看到它们的区别在于，通用的视图集GenericViewSet也是扩展了对象的处理方法，类似于GenericAPIView。

不做具体说明。



上述的视图集中可以看到都有一个共同的类`ViewSetMixin`,下面来说说这个类。

## `ViewSetMixin`

```python
class ViewSetMixin:
    """
    This is the magic.

    Overrides `.as_view()` so that it takes an `actions` keyword that performs
    the binding of HTTP methods to actions on the Resource.

    For example, to create a concrete view binding the 'GET' and 'POST' methods
    to the 'list' and 'create' actions...

    view = MyViewSet.as_view({'get': 'list', 'post': 'create'})
    """

    @classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        """
        Because of the way class based views create a closure around the
        instantiated view, we need to totally reimplement `.as_view`,
        and slightly modify the view function that is created and returned.
        """
        # The name and description initkwargs may be explicitly overridden for
        # certain route configurations. eg, names of extra actions.
        cls.name = None
        cls.description = None

        # The suffix initkwarg is reserved for displaying the viewset type.
        # This initkwarg should have no effect if the name is provided.
        # eg. 'List' or 'Instance'.
        cls.suffix = None

        # The detail initkwarg is reserved for introspecting the viewset type.
        cls.detail = None

        # Setting a basename allows a view to reverse its action urls. This
        # value is provided by the router through the initkwargs.
        cls.basename = None

        # actions must not be empty
        if not actions:
            raise TypeError("The `actions` argument must be provided when "
                            "calling `.as_view()` on a ViewSet. For example "
                            "`.as_view({'get': 'list'})`")

        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r" % (
                    cls.__name__, key))

        # name and suffix are mutually exclusive
        if 'name' in initkwargs and 'suffix' in initkwargs:
            raise TypeError("%s() received both `name` and `suffix`, which are "
                            "mutually exclusive arguments." % (cls.__name__))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)

            if 'get' in actions and 'head' not in actions:
                actions['head'] = actions['get']

            # We also store the mapping of request methods to actions,
            # so that we can later set the action attribute.
            # eg. `self.action = 'list'` on an incoming GET request.
            self.action_map = actions

            # Bind methods to actions
            # This is the bit that's different to a standard view
            for method, action in actions.items():
                handler = getattr(self, action)
                setattr(self, method, handler)

            self.request = request
            self.args = args
            self.kwargs = kwargs

            # And continue as usual
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())

        # We need to set these on the view function, so that breadcrumb
        # generation can pick out these bits of information from a
        # resolved URL.
        view.cls = cls
        view.initkwargs = initkwargs
        view.actions = actions
        return csrf_exempt(view)
```



