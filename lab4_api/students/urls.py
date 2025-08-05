from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.student_list),
    path('students/<int:id>/', views.student_detail),
    path('students/create/', views.student_create),
    path('students/<int:id>/update/', views.student_update),
    path('students/<int:id>/delete/', views.student_delete),
    path('courses/<int:id>/students/', views.students_in_course),  # Bonus
]
