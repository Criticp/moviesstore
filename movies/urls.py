from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),

    # Reviews (existing)
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),

    # S–Z user story: hidden movies
    path('hidden/', views.hidden_list, name='movies.hidden'),
    path('<int:id>/hide-toggle/', views.hide_toggle, name='movies.hide_toggle'),
]
