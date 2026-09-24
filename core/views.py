from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from .models import (
    CategorieJournaliste, CategorieActualite, Journaliste, 
    Stagiaire, Actualite, Partenaire, MessageContact
)
from .forms import (
    LoginForm, JournalisteRegistrationForm, StagiaireRegistrationForm, 
    ActualiteForm, ProfileUpdateForm, ContactForm
)

def accueil(request):
    latest_actualites = Actualite.objects.filter(approuve=True)[:6]
    featured_journalistes = Journaliste.objects.filter(approuve=True)[:4]
    context = {'active_page': 'accueil', 'latest_actualites': latest_actualites, 'featured_journalistes': featured_journalistes}
    return render(request, 'accueil.html', context)

def presentation(request):
    context = {'active_page': 'presentation'}
    return render(request, 'presentation.html', context)

def actualites_list(request):
    categories = CategorieActualite.objects.all()
    selected_category = request.GET.get('categorie', None)
    actualites = Actualite.objects.filter(approuve=True)
    if selected_category:
        actualites = actualites.filter(categorie__id=selected_category)
    context = {'active_page': 'actualites', 'actualites': actualites, 'categories': categories, 'selected_category': int(selected_category) if selected_category else None}
    return render(request, 'actualites.html', context)

def actualite_detail(request, slug):
    actualite = get_object_or_404(Actualite, slug=slug, approuve=True)
    related = Actualite.objects.filter(approuve=True, categorie=actualite.categorie).exclude(id=actualite.id)[:3]
    context = {'actualite': actualite, 'related_actualites': related}
    return render(request, 'actualite_detail.html', context)

def journalistes_list(request):
    journalistes = Journaliste.objects.filter(approuve=True)
    categories = CategorieJournaliste.objects.all()
    context = {'active_page': 'journalistes', 'journalistes': journalistes, 'categories': categories}
    return render(request, 'journalistes.html', context)

def journaliste_detail(request, pk):
    journaliste = get_object_or_404(Journaliste, pk=pk, approuve=True)
    actualites = Actualite.objects.filter(journaliste=journaliste, approuve=True)
    context = {'journaliste': journaliste, 'actualites': actualites}
    return render(request, 'journaliste_detail.html', context)

def partenaires_list(request):
    partenaires = Partenaire.objects.filter(actif=True)
    context = {'active_page': 'partenaires', 'partenaires': partenaires}
    return render(request, 'partenaires.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user_obj = User.objects.get(email=email)
                user_obj = authenticate(username=user_obj.username, password=password)
                if user_obj is not None:
                    if request.user.is_authenticated:
                        logout(request)
                    login(request, user_obj)
                    # Rediriger selon le type d'utilisateur
                    try:
                        user_obj.journaliste
                        return redirect('core:dashboard')
                    except Journaliste.DoesNotExist:
                        if user_obj.is_staff:
                            return redirect('/admin/')
                        return redirect('core:accueil')
                else:
                    messages.error(request, 'Identifiants invalides.')
            except User.DoesNotExist:
                messages.error(request, 'Aucun compte trouvé avec cette adresse email.')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})


def csrf_failure_view(request, reason=''):
    """Page professionnelle en cas d'erreur CSRF (au lieu de la page Django par défaut)."""
    return render(request, 'csrf_error.html', status=403)

def logout_view(request):
    logout(request)
    return redirect('core:accueil')

def register_journalist(request):
    if request.method == 'POST':
        form = JournalisteRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre demande a été soumise. Un administrateur examinera votre profil.')
            return redirect('core:accueil')
    else:
        form = JournalisteRegistrationForm()
    return render(request, 'register_journalist.html', {'form': form})

def register_trainee(request):
    if request.method == 'POST':
        form = StagiaireRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre demande a été soumise. Un administrateur examinera votre profil.')
            return redirect('core:accueil')
    else:
        form = StagiaireRegistrationForm()
    return render(request, 'register_trainee.html', {'form': form})

@login_required
def dashboard(request):
    try:
        journaliste = request.user.journaliste
    except Journaliste.DoesNotExist:
        messages.error(request, 'Vous n\'avez pas de profil journaliste associé.')
        return redirect('core:accueil')
        
    context = {'journaliste': journaliste, 'active_page': 'dashboard'}
    return render(request, 'dashboard/menu.html', context)

@login_required
def publish_news(request):
    try:
        journaliste = request.user.journaliste
    except Journaliste.DoesNotExist:
        return redirect('core:accueil')
        
    if request.method == 'POST':
        form = ActualiteForm(request.POST, request.FILES)
        if form.is_valid():
            actualite = form.save(commit=False)
            actualite.journaliste = journaliste
            actualite.approuve = False
            actualite.save()
            messages.success(request, 'Actualité soumise. En attente de validation.')
            return redirect('core:my_news')
    else:
        form = ActualiteForm()
        
    return render(request, 'dashboard/publish_news.html', {'form': form})

@login_required
def my_news(request):
    try:
        journaliste = request.user.journaliste
    except Journaliste.DoesNotExist:
        return redirect('core:accueil')
        
    actualites = Actualite.objects.filter(journaliste=journaliste)
    return render(request, 'dashboard/my_news.html', {'actualites': actualites})

@login_required
def edit_news(request, pk):
    try:
        journaliste = request.user.journaliste
    except Journaliste.DoesNotExist:
        return redirect('core:accueil')
        
    actualite = get_object_or_404(Actualite, pk=pk, journaliste=journaliste)
    
    if request.method == 'POST':
        form = ActualiteForm(request.POST, request.FILES, instance=actualite)
        if form.is_valid():
            act = form.save(commit=False)
            act.approuve = False
            act.save()
            messages.success(request, 'Actualité modifiée. En attente de validation.')
            return redirect('core:my_news')
    else:
        form = ActualiteForm(instance=actualite)
        
    return render(request, 'dashboard/edit_news.html', {'form': form, 'actualite': actualite})

@login_required
def toggle_news(request, pk):
    try:
        journaliste = request.user.journaliste
    except Journaliste.DoesNotExist:
        return redirect('core:accueil')
        
    actualite = get_object_or_404(Actualite, pk=pk, journaliste=journaliste)
    actualite.approuve = False
    actualite.status = 'Désactivé par le journaliste'
    actualite.save()
    messages.success(request, 'Actualité désactivée.')
    return redirect('core:my_news')

@login_required
def my_scores(request):
    try:
        journaliste = request.user.journaliste
    except Journaliste.DoesNotExist:
        return redirect('core:accueil')
        
    actualites = Actualite.objects.filter(journaliste=journaliste)
    stats = {
        'total': actualites.count(), 
        'approuvees': actualites.filter(approuve=True).count(), 
        'en_attente': actualites.filter(approuve=False).count()
    }
    
    evaluated_actualites = actualites.filter(evaluation__gt=0)
    if evaluated_actualites.exists():
        stats['avg_note'] = sum(a.note for a in evaluated_actualites) / evaluated_actualites.count()
        stats['avg_performances'] = sum(a.performances for a in evaluated_actualites) / evaluated_actualites.count()
        stats['avg_normes'] = sum(a.normes for a in evaluated_actualites) / evaluated_actualites.count()
        stats['avg_evaluation'] = sum(a.evaluation for a in evaluated_actualites) / evaluated_actualites.count()
        
    return render(request, 'dashboard/my_scores.html', {'actualites': actualites, 'stats': stats})

@login_required
def my_profile(request):
    try:
        journaliste = request.user.journaliste
    except Journaliste.DoesNotExist:
        return redirect('core:accueil')
        
    return render(request, 'dashboard/my_profile.html', {'journaliste': journaliste})

@login_required
def update_profile(request):
    try:
        journaliste = request.user.journaliste
    except Journaliste.DoesNotExist:
        return redirect('core:accueil')
        
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=journaliste)
        if form.is_valid():
            j = form.save(commit=False)
            j.approuve = False
            j.save()
            messages.success(request, 'Profil mis à jour. En attente de validation.')
            return redirect('core:my_profile')
    else:
        form = ProfileUpdateForm(instance=journaliste)
        
    return render(request, 'dashboard/my_profile.html', {'form': form, 'editing': True, 'journaliste': journaliste})

@login_required
def deactivate_profile(request):
    try:
        journaliste = request.user.journaliste
    except Journaliste.DoesNotExist:
        return redirect('core:accueil')
        
    journaliste.approuve = False
    journaliste.save()
    messages.success(request, 'Votre profil a été désactivé.')
    return redirect('core:my_profile')

def about(request):
    context = {'active_page': 'about'}
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a bien été envoyé.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'active_page': 'contact'})
