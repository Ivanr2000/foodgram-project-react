from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

username_validator = UnicodeUsernameValidator()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("У пользователя должен быть указан адрес "
                             "электронной почты")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        superuser = self.create_user(
            email,
            password=password,
            **extra_fields,
        )
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser


class CustomUser(AbstractUser):
    username = models.CharField(
        'Имя польователя',
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(
        verbose_name='Эл. почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    is_active = models.BooleanField('Активный', default=True)
    is_staff = models.BooleanField('Персонал', default=False)
    is_admin = models.BooleanField('Администратор', default=False)

    custom_objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password'
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.email

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
