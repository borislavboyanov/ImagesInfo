from django.db import models

# Create your models here.

class ImageData(models.Model):
    class Meta:
        db_table = 'image_data'
    
    id = models.AutoField(primary_key=True)
    sha1 = models.CharField(max_length=40)
    width = models.IntegerField()
    height = models.IntegerField()
    type = models.CharField(max_length=10)
