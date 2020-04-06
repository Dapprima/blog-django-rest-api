import datetime

from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from .serializers import PostSerializer, LikeSerializer, UnlikeSerializer
from .decorators import user_activity, IsOwner
from .models import Post, Like, Unlike, UserActivity

@user_activity
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def apiOverview(request):
    api_urls = {
        'Register': '/api/auth/register/',
        'Login and obtain token': '/api/auth/token/',
        'Refresh token': '/api/auth/token/refresh/',
        'Post list': 'api/posts/',
        'Post Create': 'api/post/',
        'Post Delete, Update, Retrieve': 'api/post/pk/',
        'Post like': 'api/post/pk/like/',
        'Post unlike': 'api/post/pk/unlike/',
        'Post like analitics': 'api/post/pk/start/end/',
        'User activity': 'api/user/pk/',
    }

    return Response(api_urls, status=status.HTTP_200_OK)


# Create post list with all posts
@method_decorator(user_activity, name='dispatch')
class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


# Create post
@method_decorator(user_activity, name='dispatch')
class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Add  request user like post author
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Post delete, update, retrieve
@method_decorator(user_activity, name='dispatch')
class PostView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post
    permission_classes = [permissions.IsAuthenticated, IsOwner]


# Add like to post
@method_decorator(user_activity, name='dispatch')
class LikeCreateView(CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(
            author = request.user,
            post = post
        )
        post.likes.add(like)
        return Response(status=status.HTTP_200_OK)

#Add unlike to post
@method_decorator(user_activity, name='dispatch')
class UnlikeCreateView(CreateAPIView):
    serializer_class = UnlikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        unlike, created = Unlike.objects.get_or_create(
            author = request.user,
            post = post
        )
        post.unlikes.add(unlike)
        return Response(status=status.HTTP_200_OK)
        


# Get post like analitics between dates
@user_activity
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def post_analitics(request, pk, start, end):
    try:
        datetime.datetime.strptime(start, '%Y-%m-%d')
        datetime.datetime.strptime(end, '%Y-%m-%d')
        if start > end:
            raise ValueError
    except ValueError:
        error = {
            "detail":"Incorrect data format, should be YYYY-MM-DD and start date must be \
            lower then and date"
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST)
    # Check if post exist
    get_object_or_404(Post, pk=pk)

    likes = Like.objects.filter(post__id=pk, created_at__gte = start, created_at__lte = end)\
        .extra({'date': 'date(created_at)'}).values('date').annotate(count=Count('created_at'))\
        .order_by('-created_at')

    countArray = []

    for like in likes:
        data = {'date': str(like['date']), 'likes_count': like['count']}
        countArray.append(data)

    return Response(countArray, status=status.HTTP_200_OK)


# Get user activity information
@user_activity
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_activity(request, pk):
    user = get_object_or_404(User, pk=pk)
    last_login = user.last_login
    last_request = UserActivity.objects.get(id=pk).last_request
    user_info = {
        'id': user.id,
        'last_login': last_login,
        'last_request': last_request
    }
    return Response(user_info, status=status.HTTP_200_OK)