from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from myapp.system.models import Comment, User
from myapp.system.serializer import CommentSerializer, UserCommentSerializer

class CommentGenericAPIView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    def get(self,request,*args,**kwargs):
        instance = self.get_queryset()
        # 添加上下文信息
        serializer = self.get_serializer(instance, many=True, context={'url':request.build_absolute_uri()})
        return Response(serializer.data)
    
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserCommentGenericAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserCommentSerializer

    def get(self,request,*args,**kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)