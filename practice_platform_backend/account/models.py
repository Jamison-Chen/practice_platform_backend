import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from . import UserIdentity


class CreateUpdateDate(models.Model):
    """
    Abstract base class with a creation and modification date and time
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password, identity, **extra_fields):
        # `normalize_email` is a class method
        email = UserManager.normalize_email(email)

        # Google OAuth2 backend send unnecessary username field
        # extra_fields.pop("username", None)

        user = self.model(
            email=email,
            identity=identity,
            is_staff=identity == UserIdentity.QUISHOP_STAFF,
            is_superuser=identity == UserIdentity.QUISHOP_STAFF,
            **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_customer(self, email, password, **extra_fields):
        return self.create_user(
            email, password, identity=UserIdentity.CUSTOMER, **extra_fields
        )

    def create_tenant_user(self, email, password, **extra_fields):
        return self.create_user(
            email, password, identity=UserIdentity.TENANT_STAFF, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        # Only QuiShop staff can be superusers.
        return self.create_user(
            email, password, identity=UserIdentity.QUISHOP_STAFF, **extra_fields
        )

    def all_customers(self):
        return self.get_queryset().filter(is_staff=False, is_active=True)

    def all_staff(self):
        # Select only staff of the current tenant.
        return self.get_queryset().filter(identity=UserIdentity.TENANT_STAFF)


class user(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=256, unique=True)
    username = models.CharField(max_length=256, unique=False)
    first_name = None  # remove this default column of AbstracUser
    last_name = None  # remove this default column of AbstracUser
    identity = models.CharField(max_length=16, choices=UserIdentity.CHOICES)
    avatar = models.ImageField(upload_to="user-avatars/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    # Implementation of AbstractUser
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
