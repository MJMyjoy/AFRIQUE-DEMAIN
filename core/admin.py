from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import (
    CategorieJournaliste, CategorieActualite, Journaliste,
    Stagiaire, Actualite, Partenaire, MessageContact
)


@admin.register(CategorieJournaliste)
class CategorieJournalisteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'couleur']

@admin.register(CategorieActualite)
class CategorieActualiteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'couleur']


# ── Journaliste Admin avec champ mot de passe ──────────────────────

class JournalisteAdminForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        label='Mot de passe',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez un mot de passe pour ce journaliste'}),
        help_text='Remplissez ce champ pour créer ou modifier le mot de passe de connexion. Laissez vide pour ne pas changer.'
    )

    class Meta:
        model = Journaliste
        fields = '__all__'


@admin.register(Journaliste)
class JournalisteAdmin(admin.ModelAdmin):
    form = JournalisteAdminForm
    list_display = ['prenom', 'nom', 'type_journaliste', 'email', 'matricule', 'performances', 'approuve', 'has_account', 'date_inscription']
    list_filter = ['type_journaliste', 'approuve', 'categorie', 'nationalite']
    search_fields = ['prenom', 'nom', 'email', 'matricule']
    list_editable = ['approuve']
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('prenom', 'nom', 'nationalite', 'ville_residence', 'region', 'lieu_service', 'departement', 'fonctions', 'photo_profil', 'email', 'telephone', 'bio', 'medias')
        }),
        ('Classification', {
            'fields': ('type_journaliste', 'categorie')
        }),
        ('Administration', {
            'fields': ('matricule', 'performances', 'approuve'),
        }),
        ('Compte de connexion', {
            'fields': ('mot_de_passe',),
            'description': 'Entrez un mot de passe pour permettre au journaliste de se connecter avec son email. Le compte utilisateur sera créé automatiquement.',
        }),
    )
    actions = ['approuver_journalistes', 'desapprouver_journalistes']

    @admin.display(boolean=True, description='Compte actif')
    def has_account(self, obj):
        return obj.user is not None

    def save_model(self, request, obj, form, change):
        mot_de_passe = form.cleaned_data.get('mot_de_passe')
        if mot_de_passe:
            if obj.user:
                # Mise à jour du mot de passe existant
                obj.user.set_password(mot_de_passe)
                obj.user.save()
            else:
                # Création d'un nouveau User
                user = User.objects.create_user(
                    username=obj.email,
                    email=obj.email,
                    password=mot_de_passe,
                    first_name=obj.prenom,
                    last_name=obj.nom,
                )
                obj.user = user
        super().save_model(request, obj, form, change)

    def approuver_journalistes(self, request, queryset):
        queryset.update(approuve=True)
    approuver_journalistes.short_description = 'Approuver les journalistes selectionnes'

    def desapprouver_journalistes(self, request, queryset):
        queryset.update(approuve=False)
    desapprouver_journalistes.short_description = 'Desapprouver les journalistes selectionnes'


# ── Stagiaire Admin avec champ mot de passe ────────────────────────

class StagiaireAdminForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        label='Mot de passe',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez un mot de passe pour ce stagiaire'}),
        help_text='Remplissez ce champ pour créer ou modifier le mot de passe de connexion. Laissez vide pour ne pas changer.'
    )

    class Meta:
        model = Stagiaire
        fields = '__all__'


@admin.register(Stagiaire)
class StagiaireAdmin(admin.ModelAdmin):
    form = StagiaireAdminForm
    list_display = ['prenom', 'nom', 'post_nom', 'email', 'matricule', 'nom_responsable', 'performances', 'approuve', 'has_account', 'date_inscription']
    list_filter = ['approuve', 'niveau_academique', 'sexe', 'nationalite']
    search_fields = ['prenom', 'nom', 'post_nom', 'email', 'matricule']
    list_editable = ['approuve']
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('prenom', 'nom', 'post_nom', 'nationalite', 'ville_residence', 'commune', 'age', 'sexe', 'interet', 'photo_profil', 'email', 'telephone', 'niveau_academique', 'etat_civil', 'bio')
        }),
        ('Formation', {
            'fields': ('nom_responsable', 'tel_responsable', 'performances')
        }),
        ('Administration', {
            'fields': ('matricule', 'approuve'),
        }),
        ('Compte de connexion', {
            'fields': ('mot_de_passe',),
            'description': 'Entrez un mot de passe pour permettre au stagiaire de se connecter.',
        }),
    )

    @admin.display(boolean=True, description='Compte actif')
    def has_account(self, obj):
        return obj.user is not None

    def save_model(self, request, obj, form, change):
        mot_de_passe = form.cleaned_data.get('mot_de_passe')
        if mot_de_passe:
            if obj.user:
                obj.user.set_password(mot_de_passe)
                obj.user.save()
            else:
                user = User.objects.create_user(
                    username=obj.email,
                    email=obj.email,
                    password=mot_de_passe,
                    first_name=obj.prenom,
                    last_name=obj.nom,
                )
                obj.user = user
        super().save_model(request, obj, form, change)


# ── Actualite Admin ────────────────────────────────────────────────

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'journaliste', 'categorie', 'date', 'note', 'evaluation', 'approuve', 'date_publication']
    list_filter = ['approuve', 'categorie', 'date']
    search_fields = ['titre', 'contenu', 'journaliste__nom', 'journaliste__prenom']
    list_editable = ['approuve']
    prepopulated_fields = {'slug': ('titre',)}
    fieldsets = (
        ('Contenu', {'fields': ('journaliste', 'titre', 'slug', 'illustration', 'categorie', 'contenu', 'lieu', 'tache_effectuee', 'date', 'heure_debut', 'heure_fin', 'description_mission', 'status')}),
        ('Evaluation', {'fields': ('note', 'performances', 'normes', 'evaluation', 'commentaires_correcteurs'), 'classes': ['collapse']}),
        ('Publication', {'fields': ('approuve',)}),
    )
    readonly_fields = ['evaluation']
    actions = ['approuver_actualites', 'desapprouver_actualites']

    def approuver_actualites(self, request, queryset):
        queryset.update(approuve=True)
    approuver_actualites.short_description = 'Approuver les actualites selectionnees'

    def desapprouver_actualites(self, request, queryset):
        queryset.update(approuve=False)
    desapprouver_actualites.short_description = 'Desapprouver les actualites selectionnees'


@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ['nom', 'site_web', 'actif', 'ordre']
    list_editable = ['actif', 'ordre']

@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ['sujet', 'nom', 'email', 'date_envoi', 'lu']
    list_filter = ['lu', 'date_envoi']
    list_editable = ['lu']
    readonly_fields = ['nom', 'email', 'sujet', 'message', 'date_envoi']
