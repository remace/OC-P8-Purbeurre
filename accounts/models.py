from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

from products.models import Product


class UserManager(BaseUserManager):
    """ User Model Manager """
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        # authentification keys verification
        if not email:
            raise ValueError('Users must have email Address')
        if not password:
            raise ValueError('User must have Password')
        
        user_obj = self.model(
            email=self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.save(using=self._db)


    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    ''' user model '''
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    email= models.EmailField(unique=True)
    phone = PhoneNumberField(null=True)
    # TODO AVATAR ?
    
    # registration create and update fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # for deletion
    is_active = models.BooleanField(default=True)

    # permissions
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    #use email for authentification
    USERNAME_FIELD = 'email'

    #relation to save favourite products
    favourites = models.ManyToManyField(Product,related_name='products',blank=False)

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name:
            return f'{self.first_name}  {self.last_name}'
        return self.email.split('@')[0]

    def has_perm(self, perm, obj=None):
        return True
        
    def has_module_perms(self, app_label):
        return True