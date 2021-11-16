from django.db.models.signals import post_save
import json
import os
from .action_controller import generate_image_data
from .models import ImageData
from .models import User

# def process_images(sender, instance, **kwargs):
#     images = ImageData.objects.filter(sha1 = None)
#
#     for image in images:
#         try:
#             file = open('./image_files/' + image.name, 'rb+')
#         except:
#             continue
#         data = generate_image_data(file)
#         data = json.loads(data.content)
#         name = image.name
#         if data['status'] == 400:
#             image.delete()
#             os.remove(name)
#             continue
#         image.name b782594706d8= None
#         image.sha1 = data['sha1']
#         image.width = data['width']
#         image.height = data['height']
#         image.type = data['type']
#
#         image.save()
#         file.close()
#         os.remove(name)

def process_images(sender, instance, created, **kwargs):
    if created:
        try:
            file = open('./image_files/' + instance.name, 'rb+')
        except:
            return
        data = generate_image_data(file)
        data = json.loads(data.content)
        name = instance.name
        if data['status'] == 400:
            instance.delete()
            os.remove(name)
            return
        instance.name = None
        instance.sha1 = data['sha1']
        instance.width = data['width']
        instance.height = data['height']
        instance.type = data['type']
        try:
            instance.save()
        except:
            pass

        file.close()
        os.remove('./image_files/' + name)

post_save.connect(process_images, sender=ImageData)
