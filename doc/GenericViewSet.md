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