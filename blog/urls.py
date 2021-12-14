from django.urls import path
from . import views

urlpatterns = [
    path("",views.StartPageView.as_view(),name="starting_page"),
    path("posts",views.AllPostsView.as_view(),name="posts"),
    path("posts/<slug:slug>",views.PostDetailView.as_view(),name="post_details"),
    path("read-later",views.ReadLaterView.as_view(),name="read-later")
]
