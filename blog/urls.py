from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("user/<str:username>/", views.UserPostListView.as_view(), name="user_posts"),
    path("like/", views.like_post, name="like_post"),

    path("post/new/", views.PostCreateView.as_view(), name="post_create"),

    path("gotopage/", views.gotopage, name="gotopage"),
    path("about/", views.about, name="about"),
    path("visit/", views.visits, name="visits"),

]