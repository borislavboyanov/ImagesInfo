import json
import os
from .action_controller import generate_image_data
from .models import ImageData

def work_with_images():
    images = ImageData.objects.filter(sha1 = None)

    for image in images:
        try:
            file = open(image.name, 'rb+')
        except:
            continue
        data = generate_image_data(file.read())
        data = json.loads(data.content)
        name = image.name
        if data['status'] == 400:
            image.delete()
            os.remove(name)
            continue
        image.name = None
        image.sha1 = data['sha1']
        image.width = data['width']
        image.height = data['height']
        image.type = data['type']

        image.save()
        file.close()
        os.remove(name)
