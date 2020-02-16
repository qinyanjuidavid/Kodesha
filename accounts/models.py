from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class custommanager(BaseUserManager):
    def create_user(self,email,username,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('Users must have an email.')

        if not password:
            raise ValueError("Users must have a password.")

        if not username:
            raise ValueError("Users must have a username.")

        user_obj=self.model(
        email=self.normalize_email(email),
        username=username
        )
        user_obj.set_password(password)
        user_obj.active=is_active
        user_obj.admin=is_admin
        user_obj.staff=is_staff
        user_obj.save(using=self._db)

        return user_obj

    def create_staff(self,email,username,password=None):
        user=self.create_user(
        email,
        username,
        password=password,
        is_staff=True
        )
        return user

    def create_superuser(self,email,username,password=None):
        user=self.create_user(
        email,
        username,
        password=password,
        is_staff=True,
        is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email=models.EmailField(max_length=255, unique=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    admin=models.BooleanField(default=False)
    username=models.CharField(max_length=30)
    staff=models.BooleanField(default=False)
    active=models.BooleanField(default=True)

    USERNAME_FIELD='email'

    REQUIRED_FIELDS=['username']

    objects=custommanager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default1.jpg', upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile'
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        profile,new=Profile.objects.get_or_create(user=instance)
