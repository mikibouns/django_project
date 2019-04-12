from django.db import models

# Create your models here.


class Collection(models.Model):
    name = models.CharField(max_length=128)
    img = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Wallpaper(models.Model):
    article = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    preview_img = models.ImageField()
    img = models.ImageField(null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.article)


class Interior(models.Model):
    name = models.CharField(max_length=128)
    img = models.ImageField()

    def __str__(self):
        return self.name
