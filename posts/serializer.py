from rest_framework import serializers

from account.models import User
from account.serializers import ProfessionalProfileSerilaizer, UserProfileSerializer,UserSerializer

from .models import Comment, Like, Post


class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class LikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class CommentSerializer(serializers.ModelSerializer):
    # user = CommentUserSerializer(read_only=True)
    # userprofile = UserProfileSerializer(source="user.userprofile", required=False)
    # professionalprofile = ProfessionalProfileSerilaizer(
    #     source="user.professionalprofile", required=False
    # )

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "user",
            "text",
            "created_at",
            # "userprofile",
            # "professionalprofile",
        ]
        # read_only_fields = ("user",)

    def create(self, validated_data):
        return super().create(validated_data)

    


class LikeSerializer(serializers.ModelSerializer):
    # user = LikeUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ("user", "post", "created_at")
        # read_only_fields = ("user",)


class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer()
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "user",
            "post",
            "created_at",
            "description",
            "likes",
            "comments",
        )
        read_only_fields = ("user",)

    def create(self, validated_data):
        return super(PostSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        # instance.post = validated_data.get('post',instance.post)
        instance.description = validated_data.get("description", instance.description)

        return super().update(instance, validated_data)

    def get_total_likes(self, post):
        return post.likes.count()

# class PostSerializer(serializers.ModelSerializer):
#     likes = LikeSerializer(many=True, read_only=True)
#     comments = CommentSerializer(many=True, read_only=True)
#     # userprofile = UserProfileSerializer(source="user.userprofile", required=False)
#     # professionalprofile = ProfessionalProfileSerilaizer(
#     #     source="user.professionalprofile", required=False
#     # )

#     class Meta:
#         model = Post
#         fields = (
#             "id",
#             "title",
#             # "user",
#             "post",
#             "created_at",
#             "description",
#             "likes",
#             "comments",
#             # "userprofile",
#             # "professionalprofile",
#         )