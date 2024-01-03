from django.urls import path
from . import views 




urlpatterns = [
    path('allpost/', views.AllPost.as_view(), name='posts'),
    path('post/',views.PostView.as_view(),name='post-creation'), 
    path('post/<int:pk>/update/', views.PostUpdateDelettView.as_view(), name='post-update'),
    path('post/<int:pk>/like/', views.PostLikeView.as_view(), name='like-post'),
    path('post/<int:pk>/comment/', views.CommentCreateView.as_view(), name='create-comment'),
    path('post/<int:pk>/comment/list/', views.CommentCreateView.as_view(), name='list-comments'),
    path('comment/<int:pk>/delete/', views.CommentCreateView.as_view(), name='delete-comment'),
]       
