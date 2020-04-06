from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('api/auth/', include('jwt_auth.urls'), name='jwt_auth'),
    path('api/posts/', views.PostListView.as_view(), name='posts'),  
    path('api/post/', views.PostCreateView.as_view(), name='create_post'),
    path('api/post/<str:pk>/', views.PostView.as_view(), name='post'),
    path('api/post/<str:pk>/like/', views.LikeCreateView.as_view(), name='post-like'),
    path('api/post/<str:pk>/unlike/', views.UnlikeCreateView.as_view(), name='post-unlike'),
    path('api/post/<str:pk>/<str:start>/<str:end>/', views.post_analitics, name='post-analitics'),
    path('api/user/<str:pk>/', views.user_activity, name='user-activity'),    
]
