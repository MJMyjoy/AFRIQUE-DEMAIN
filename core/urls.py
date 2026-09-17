from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('presentation/', views.presentation, name='presentation'),
    path('actualites/', views.actualites_list, name='actualites'),
    path('actualites/<slug:slug>/', views.actualite_detail, name='actualite_detail'),
    path('journalistes/', views.journalistes_list, name='journalistes'),
    path('journalistes/<int:pk>/', views.journaliste_detail, name='journaliste_detail'),
    path('partenaires/', views.partenaires_list, name='partenaires'),
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('inscription-journaliste/', views.register_journalist, name='register_journalist'),
    path('inscription-formation/', views.register_trainee, name='register_trainee'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/publier/', views.publish_news, name='publish_news'),
    path('dashboard/mes-actualites/', views.my_news, name='my_news'),
    path('dashboard/modifier-actualite/<int:pk>/', views.edit_news, name='edit_news'),
    path('dashboard/toggle-actualite/<int:pk>/', views.toggle_news, name='toggle_news'),
    path('dashboard/mes-scores/', views.my_scores, name='my_scores'),
    path('dashboard/mon-profil/', views.my_profile, name='my_profile'),
    path('dashboard/modifier-profil/', views.update_profile, name='update_profile'),
    path('dashboard/desactiver-profil/', views.deactivate_profile, name='deactivate_profile'),
    path('a-propos/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
