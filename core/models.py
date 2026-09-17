from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import random
import string

class CategorieJournaliste(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    icone = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class, e.g. fas fa-globe')
    couleur = models.CharField(max_length=7, default='#1565c0', help_text='Hex color code')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Catégorie de journaliste'
        verbose_name_plural = 'Catégories de journalistes'


class CategorieActualite(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    icone = models.CharField(max_length=50, blank=True)
    couleur = models.CharField(max_length=7, default='#1565c0')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Catégorie d\'actualité'
        verbose_name_plural = 'Catégories d\'actualités'


class Journaliste(models.Model):
    TYPE_CHOICES = [
        ('interne', 'Interne'),
        ('externe', 'Externe')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='journaliste')
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=100)
    ville_residence = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    lieu_service = models.CharField(max_length=200, blank=True)
    departement = models.CharField(max_length=100, blank=True)
    fonctions = models.CharField(max_length=200)
    matricule = models.CharField(max_length=50, blank=True)
    photo_profil = models.ImageField(upload_to='journalistes/', blank=True, null=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    bio = models.TextField('Parlez de vous', blank=True)
    type_journaliste = models.CharField(max_length=20, choices=TYPE_CHOICES, default='externe')
    performances = models.FloatField(default=0, help_text='Côte en pourcentage')
    approuve = models.BooleanField(default=False, verbose_name='Approuvé')
    categorie = models.ForeignKey(CategorieJournaliste, on_delete=models.SET_NULL, null=True, blank=True)
    medias = models.CharField(max_length=200, blank=True, help_text='Ex: Presse écrite | Web | TV')
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.prenom} {self.nom}'

    @property
    def nom_complet(self):
        return f'{self.prenom} {self.nom}'

    @property
    def performances_display(self):
        return f'{self.performances}%'

    class Meta:
        verbose_name = 'Journaliste'
        verbose_name_plural = 'Journalistes'
        ordering = ['-date_inscription']


class Stagiaire(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin')
    ]
    NIVEAU_CHOICES = [
        ('secondaire', 'Secondaire'),
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('autre', 'Autre')
    ]
    ETAT_CIVIL_CHOICES = [
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('divorce', 'Divorcé(e)'),
        ('veuf', 'Veuf/Veuve')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='stagiaire')
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    post_nom = models.CharField(max_length=100, verbose_name='Post-nom')
    nationalite = models.CharField(max_length=100)
    ville_residence = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES)
    interet = models.CharField(max_length=200, verbose_name='Intéressé par')
    photo_profil = models.ImageField(upload_to='stagiaires/', blank=True, null=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    niveau_academique = models.CharField(max_length=50, choices=NIVEAU_CHOICES)
    etat_civil = models.CharField(max_length=20, choices=ETAT_CIVIL_CHOICES)
    bio = models.TextField('Parlez de vous', blank=True)
    performances = models.FloatField(default=0)
    nom_responsable = models.CharField(max_length=200, blank=True, verbose_name='Nom du responsable/formateur')
    tel_responsable = models.CharField(max_length=20, blank=True)
    matricule = models.CharField(max_length=50, blank=True)
    approuve = models.BooleanField(default=False, verbose_name='Approuvé')
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.prenom} {self.nom}'

    class Meta:
        verbose_name = 'Stagiaire'
        verbose_name_plural = 'Stagiaires'
        ordering = ['-date_inscription']


class Actualite(models.Model):
    journaliste = models.ForeignKey(Journaliste, on_delete=models.CASCADE, related_name='actualites')
    illustration = models.ImageField(upload_to='actualites/', blank=True, null=True)
    titre = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    categorie = models.ForeignKey(CategorieActualite, on_delete=models.SET_NULL, null=True, blank=True)
    contenu = models.TextField()
    lieu = models.CharField(max_length=200)
    tache_effectuee = models.CharField(max_length=200, verbose_name='Tâche effectuée', help_text='Rédaction, reportage, prise de vue...')
    date = models.DateField()
    heure_debut = models.TimeField(verbose_name='Heure de début')
    heure_fin = models.TimeField(verbose_name='Heure de fin')
    description_mission = models.TextField(verbose_name='Décrire la mission', blank=True)
    status = models.CharField(max_length=50, default='Soumis')
    note = models.FloatField(default=0, verbose_name='Note brute', help_text='Note donnée par les correcteurs')
    performances = models.FloatField(default=0)
    normes = models.FloatField(default=0, verbose_name='Respect des normes')
    evaluation = models.FloatField(default=0, verbose_name='Évaluation', help_text='Moyenne auto-calculée')
    commentaires_correcteurs = models.TextField(blank=True, verbose_name='Commentaires des correcteurs')
    approuve = models.BooleanField(default=False, verbose_name='Approuvé')
    date_publication = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre)
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            self.slug = f"{base_slug}-{random_suffix}"
        
        if self.note > 0 or self.performances > 0 or self.normes > 0:
            self.evaluation = (self.note + self.performances + self.normes) / 3.0
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Actualité'
        verbose_name_plural = 'Actualités'
        ordering = ['-date_publication']


class Partenaire(models.Model):
    nom = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partenaires/', blank=True, null=True)
    description = models.TextField(blank=True)
    site_web = models.URLField(blank=True)
    actif = models.BooleanField(default=True)
    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Partenaire'
        verbose_name_plural = 'Partenaires'
        ordering = ['ordre']


class MessageContact(models.Model):
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    sujet = models.CharField(max_length=300)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sujet} - {self.nom}'

    class Meta:
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'
        ordering = ['-date_envoi']
