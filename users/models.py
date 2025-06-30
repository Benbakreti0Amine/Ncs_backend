from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator

class MyUserManager(BaseUserManager):
    def create_user(self, nom, prenom, numero_de_telephone, password, **kwargs):

        if not nom:
            raise ValueError('Users must have a last name')
        if not prenom:
            raise ValueError('Users must have a first name')
        if not numero_de_telephone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            nom=nom,
            prenom=prenom,
            numero_de_telephone=numero_de_telephone,
            **kwargs
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, nom, prenom, numero_de_telephone, password, **extra_fields):
        user = self.create_user(
            nom=nom,
            prenom=prenom,
            numero_de_telephone=numero_de_telephone,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')
    
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('VENDOR', 'Vendor'),
        ('RELAY_OPERATOR', 'Relay Operator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VENDOR')
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    numero_de_telephone = models.CharField(max_length=15, unique=True)

    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'numero_de_telephone'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def get_short_name(self):
        return self.prenom


