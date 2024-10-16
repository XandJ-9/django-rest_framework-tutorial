from rest_framework import serializers

class Comment(object):
    def __init__(self, content, author):
        self.content = content
        self.author = author


class CommentSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Comment(**validated_data)
    
    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.author = validated_data.get('author', instance.author)
        return instance

serailizer = CommentSerializer(Comment('hello world', 'jason'))
print(serailizer.data)  # {'content': 'hello world', 'author': 'jason'}

