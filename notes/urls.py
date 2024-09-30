from django.urls import path

from notes import views

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("register/",views.UserCreationView.as_view()),

    path("tasks/",views.TaskCreateListView.as_view()),

    path("tasks/<int:pk>/",views.RetrieveUpdateDestroyView.as_view()),

    path("tasks/summary/",views.TaskSummaryAPIView.as_view()),

    path("tasks/categories/",views.CategoryListView.as_view()),

    path("tasks/priorities/",views.PriorityListView.as_view()),

    path("token/",ObtainAuthToken.as_view()),

]