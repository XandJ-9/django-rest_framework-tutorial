from rest_framework import serializers

from myapp.system.models import User,Account,Comment


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=50)
    def create(self, validated_data):
        return User.objects.create(**validated_data)

class AccountSerializer(serializers.Serializer):
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)  # 该字段只查询，创建对象时不检查该字段
    class Meta:
      model = Account
      fields = ('username','password','create_time','update_time')

class CommentSerializer(serializers.Serializer):
  content = serializers.CharField(max_length=32)
  url = serializers.URLField()
  user = UserSerializer(required=True)

  def create(self, validated_data):
     '''
     数据保存
     '''
     user_data = validated_data.pop('user')
     user = User.objects.get(**user_data)
     instance = Comment(user_id=user.id, **validated_data)
     instance.save()
     return instance
  
  def to_representation(self, instance):
    '''
    将数据序列化展示出来
    '''
    user = User.objects.get(id=instance.user_id)
    user_ser = UserSerializer(instance = user)
    return {
      'content': instance.content,
      'url': self.context.get('url'),
      'user': user_ser.data
    }
  
class UserCommentSerializer(serializers.Serializer):
   username = serializers.CharField(max_length=32)
   comment = CommentSerializer(many=True)

   def to_representation(self, instance):
      comment_list = Comment.objects.filter(user_id=instance.id)
      comment_ser = CommentSerializer(instance=comment_list, many=True)
      return {
         'username': instance.username,
         'comment': comment_ser.data
      }