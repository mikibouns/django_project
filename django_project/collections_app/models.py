from django.db import models

# Create your models here.


class Collection(models.Model):
    name = models.CharField(max_length=128, unique=True)
    img = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name.replace(" ", "_")


class Wallpaper(models.Model):
    article = models.CharField(max_length=32, unique=True)
    description = models.TextField(null=True, blank=True)
    preview_img = models.ImageField()
    img = models.ImageField(null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)
    rapport = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ["article"]

    def __str__(self):
        return str(self.article)


class Interior(models.Model):
    name = models.CharField(max_length=128)
    img = models.ImageField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
