# below libraby for AuthToken
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# You can create your model here

class UserProfileManager(BaseUserManager):
    """Manager for user profile"""

    def create_user(self, email, username, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError('Users must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Create and save a new sueperuser with given detail"""
        user = self.create_user(email, username, password)
        user.user_type = 'Service_Provider'
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser):
    """ Database model for user in the system """
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    user_type = (
        ('as_a', 'AS A'),
        ('Customer', 'CUSTOMER'),
        ('Service_Provider', 'SERVICES PROVIDER'),
    )
    user_type = models.CharField(max_length=15, choices=user_type, default='as_a', )

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserProfileManager()

    def __str__(self):
        """Return string representation of our user"""
        return self.email

    def has_perm(self, perm, obj=None):
        """For checking permissions. to keep it simple all admin have ALL permissons"""
        return self.is_admin

    def has_module_perms(self, app_label):
        """Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)"""
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class Services(models.Model):
    servicesprovider = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Service_Provider'})
    service_name = models.CharField(max_length=100, blank=True)
    service_description = models.TextField(max_length=255, blank=True)
    service_price = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name

class ServiceRequest(models.Model):

    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'Customer'})
    service = models.ForeignKey(Services,on_delete=models.CASCADE)
    ststus = (
        ('Pending', 'PENDING'),
        ('Accepted', 'ACCEPTED'),
        ('Rejected', 'REJECTED'),
        ('Completed', 'COMPLETED'),
    )
    status = models.CharField(max_length=15, choices=ststus, default='Pending', )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.service.service_name

class Comment(models.Model):
    servicerequest = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE,limit_choices_to={'status__in': ['Accepted', 'Completed']})
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message