from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("crossroad.urls")),
    path("hello_world/", include("hello_world.urls")),
    path("habit_tracker_1/", include("habit_tracker_1.urls")),
    path("habit_tracker_2/", include("habit_tracker_2.urls")),
    path("blog/", include("blog.urls")),
    path("users/", include("users.urls")),
    path("birthday/", include("birthday.urls")),
    path("chat/", include("chat.urls")),
    path("hangman/", include("hangman.urls")),
    path("library_rest/", include("library_rest.urls")),
    path("library_graph/", include("library_graph.urls")),
    path("library_rpc/", include("library_rpc.urls")),
    # path("__reload__/", include("django_browser_reload.urls")),
]
