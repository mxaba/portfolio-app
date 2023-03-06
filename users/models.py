from django.contrib.gis.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, default='')
    home_address = models.CharField(max_length=100, default='')
    location =  models.PointField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='users/profile_pics', default='users/profile_pics/default.jpg')

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
