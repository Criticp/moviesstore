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

    path('peitions/', views.petitions_list, name='movies.petitions_list'),
    path('petitions/<int:petition_id>/vote-yes/', views.petition_vote_yes, name='movies.petition_vote_yes'),
    path('petitions/<int:petition_id>/edit/', views.petition_edit, name='movies.petition_edit'),
    path('petitions/<int:petition_id>/delete/', views.petition_delete, name='movies.petition_delete'),
]
