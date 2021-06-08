from django.urls import path
from django.views.generic.base import View, RedirectView
from . import views 

urlpatterns = [
    path('', RedirectView.as_view(url='home', permanent=False), name='index'),
    path('home/',views.home_view,name='home'),
    path('today/',views.today_view, name='today'),
    path('months/',views.months_view, name='months'),
    path('months/<str:year>/<str:month>/', views.month_view, name='month'),
    path('months/<str:year>/<str:month>/<str:day>/', views.day_view, name='day'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='task-delete'),
    path('tasks/<int:pk>/mark_done/', views.mark_done, name='done-task'),
    path('add_task/', views.add_task, name='add-task'),
    path('tasks/<int:pk>/bring_back_today/', views.bring_back_to_today, name='bring-back')
    # path('test/<str:year>/<str:month>/', views.test_view, name='test'),
]