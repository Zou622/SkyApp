from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'user_type',
        'est_valide',
        'est_actif'
    )

    list_filter = (
        'user_type',
        'est_valide',
        'est_actif'
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name'
    )

<<<<<<< HEAD
    readonly_fields = ('date_inscription', 'derniere_connexion')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Liens', {'fields': ('user_type', 'employe')}),
        ('Statut', {'fields': ('est_valide', 'est_actif')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined', 'date_inscription', 'derniere_connexion')}),
=======
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Informations supplémentaires', {
            'fields': (
                'user_type',
                'telephone',
                'adresse',
                'photo',
                'est_valide',
                'technicien',
                'commercial'
            )
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
>>>>>>> 435052a26b2376cb21df734e1cce035036c00fad
    )