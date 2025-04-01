from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("crossroad.urls")),
    path("hello_world/", include("hello_world.urls")),
    path("habit_tracker_1/", include("habit_tracker_1.urls")),
    path("habit_tracker_2/", include("habit_tracker_2.urls")),
    path("blog/", include("blog.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
