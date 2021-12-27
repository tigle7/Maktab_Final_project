from django.urls import path, re_path
from .views import *
# app_name = 'blog'

urlpatterns = [
    # path('', post_list, name='post_list'),
    path('', PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('create-post/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/comment/', add_comment, name='add_comment'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:id>/', CategoryRelated.as_view(), name='category_related'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('create-category/', CategoryCreateView.as_view(), name='category_create'),
    path('dashboard/<str:username>/', UserPostListView.as_view(), name='dashboard'),
]
