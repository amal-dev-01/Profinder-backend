from rest_framework import serializers
from .models import Post,Like,Comment
from account.models import User




class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CommentSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_at']
        read_only_fields = ('user', )



class LikeSerializer(serializers.ModelSerializer):
    user = LikeUserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ('user', 'post', 'created_at')
        read_only_fields = ('user', )

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'post', 'user', 'text', 'created_at']
#         read_only_fields = ('user', )


class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields=('id','title','user','post','created_at','description','likes','total_likes','comments')
        read_only_fields = ('user', )  


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(PostSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        # instance.post = validated_data.get('post',instance.post)
        instance.description = validated_data.get('description',instance.description)

        return super().update(instance, validated_data)


    def get_total_likes(self, post):
        return post.likes.count()
    





   