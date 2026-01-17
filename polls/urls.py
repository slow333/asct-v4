from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_poll, name="create"), # type: ignore
    path("<int:pk>/detail/", views.detail, name="detail"),
    path("<int:pk>/update/",views.update_poll, name="update"),
    path("<int:pk>/delete/", views.delete_poll, name="delete"),
    
    path("<int:pk>/results/", views.result_poll, name="results"),
    path("<int:pk>/vote/", views.vote, name="vote"),
]