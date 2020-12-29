from django.db import models


class Original(models.Model):
    image = models.ImageField(upload_to='Original_img', blank=True)
    image_url = models.URLField(max_length=400, blank=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.image


class Temp(models.Model):
    width = models.IntegerField(default=0, blank=True)
    height = models.IntegerField(default=0, blank=True)




class Modified(models.Model):
    image_m = models.FileField(upload_to='Modified_img')

