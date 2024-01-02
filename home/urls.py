from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('' , views.home),
    path('student/', views.post_student),
    path('student/<id>/', views.get_student),
    path('update-student/<id>/', views.update_student),
    path('delete-student/<id>/', views.delete_student),
    path('delete-student-alternate/', views.delete_student_alternate),
    path('get-book/', views.get_book),
    path('add-book/',views.add_book),
    path('add-category/',views.add_category)
]