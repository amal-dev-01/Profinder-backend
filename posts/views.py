from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Like, Post
from .serializer import CommentSerializer, LikeSerializer, PostSerializer

# Create your views here.


class PostView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        tags=["User Post"],
        operation_description="Get the requested user post",
        responses={200: PostSerializer, 400: "bad request", 500: "errors"},
    )
    def get(self, request, format=None):
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["User Post"],
        operation_description="Create post",
        responses={200: PostSerializer, 400: "bad request", 500: "errors"},
        request_body=PostSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateDelettView(APIView):
    permission_classes = (IsAuthenticated,)

    # @swagger_auto_schema(
    #     tags=["User update post"],
    #     operation_description="Get the details of post",
    #     responses={200: PostSerializer, 400: "bad request", 500: "errors"},
    #     request_body=PostSerializer,
    # )
    def get(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        tags=["User update post"],
        operation_description="update post",
        responses={200: PostSerializer, 400: "bad request", 500: "errors"},
        request_body=PostSerializer,
    )
    def put(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["User update post"],
        operation_description="Delete post",
        responses={200: PostSerializer, 400: "bad request", 500: "errors"},
        request_body=PostSerializer,
    )
    def delete(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk, user=request.user)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found or permission denied"},
                status=status.HTTP_404_NOT_FOUND,
            )
        post.delete()
        return Response(
            {"msg": "Post sucessfully deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class AllPost(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        posts = Post.objects.exclude(user=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            Like.objects.get(post__pk=pk, user=request.user)
            return Response({"liked": True}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"liked": False}, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        like = post.likes.filter(user=request.user).first()

        if like:
            like.delete()
            return Response({"msg": "You unliked the post"}, status=status.HTTP_200_OK)
        else:
            like = Like(user=request.user, post=post)
            like.save()
            LikeSerializer(like)
            return Response(
                {"msg": "You liked the post"}, status=status.HTTP_201_CREATED
            )


class CommentCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data={"post": pk, **request.data})
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user != comment.user:
            return Response(
                {"error": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        comment.delete()
        return Response(
            {"message": "Comment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
