from django.db import models
from accounts.models import User



class House(models.Model):
    owner=models.CharField(max_length=30,default="Day Light Properties Limited")
    location=models.CharField(max_length=20)
    image=models.ImageField(upload_to="property")
    price=models.FloatField(default=0.00)
    description=models.TextField(blank=True,null=True)
    contact_email=models.EmailField(max_length=150,default="daylightproperties@gmail.com")
    contact_phone=models.CharField(max_length=20,default="0700215645")
    sold=models.BooleanField(default=False)
    likes=models.ManyToManyField(User,blank=True)
    display_image1=models.ImageField(upload_to="display",blank=True,null=True)
    display_image2=models.ImageField(upload_to='display',blank=True,null=True)
    display_image3=models.ImageField(upload_to='display',blank=True,null=True)
    display_image4=models.ImageField(upload_to='display',blank=True,null=True)

    def __str__(self):
        return f'{self.location}-->{self.price}'

    class Meta:
        verbose_name_plural="house"

class Interesting_house(models.Model):
    house=models.ForeignKey(House,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} is interested with this house worth $ {self.house.price}'
class Dashboard(models.Model):
    houses=models.ManyToManyField(Interesting_house)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    started_date=models.DateTimeField(auto_now_add=True)
    date_added=models.DateTimeField()


    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural="Dashboard"
