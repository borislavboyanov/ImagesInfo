from django.db import models

# Create your models here.

class User(models.Model):
    class Meta:
        db_table = 'users'

    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=100)

class ImageData(models.Model):
    class Meta:
        db_table = 'image_data'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    sha1 = models.CharField(max_length=40, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
