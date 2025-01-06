from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class AppUserManager(BaseUserManager):  #-----------------------------------------------------------------------------------------------------
#Tento kód definuje správce uživatelů pro model uživatele (AppUserManager), ale neobsahuje definici samotného modelu uživatele (AppUser).
# který je umístěn v models.oy  
    """
    Správce uživatelů pro model AppUser.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError(_('User must have a username'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('position', 1)  # Superuser má pozici "Manager"

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        return self.create_user(username, email, password, **extra_fields)
#---------------------------------------------------------------------------------------------------------------------------------------------
#Tento kód definuje správce uživatelů pro model uživatele (AppUserManager), ale neobsahuje definici samotného modelu uživatele (AppUser).