from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Like, Post
from .serializer import CommentSerializer, PostSerializer

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
        try:
            posts = Post.objects.filter(user=request.user).select_related('user').prefetch_related('likes', 'comments')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(
                {"error": "No posts found for the current user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        tags=["User Post"],
        operation_description="Create post",
        responses={200: PostSerializer, 400: "bad request", 500: "errors"},
        request_body=PostSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateDelettView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            post = Post.objects.prefetch_related('likes', 'comments').get(pk=pk)
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
        try:
            posts = Post.objects.exclude(user=request.user).select_related('user').prefetch_related('likes', 'comments')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            Like.objects.get(post__pk=pk, user=request.user)
            return Response({"liked": True}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"liked": False}, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            like = post.likes.filter(user=request.user).first()
            if like:
                like.delete()
                return Response(
                    {"msg": "You unliked the post"}, status=status.HTTP_200_OK
                )
            else:
                like = Like(user=request.user, post=post)
                like.save()
                return Response(
                    {"msg": "You liked the post"}, status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommentCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            comments = Comment.objects.filter(post=post).order_by("-id")
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, pk, format=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        request.data['post'] = pk
        # request.data['user'] = request.user.id
        print(request.data)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

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
