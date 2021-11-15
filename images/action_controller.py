from django.http import JsonResponse
from django.db.models.signals import post_save
import io
import json
from PIL import Image
import hashlib
import svglib.svglib as svg
from .models import ImageData
import images.signals

class NotAnImage(Exception):
    def __init__(self, message='The provided link is not of an image'):
        self.message = message
        super().__init__(self.message)

def generate_image_data(image):
    file = svg.svg2rlg(image)
    if not hasattr(file, 'height'):
        try:
            img = Image.open(image)
            if hasattr(img, 'format'):
                image_type = img.format.lower()
                width, height = img.size
            else:
                raise NotAnImage
        except NotAnImage as e:
            return JsonResponse({'response': 'Sorry, the provided link is not of an image.', 'status': 400}, safe = False)
    else:
        image_type = 'svg'
        width = int(file.width)
        height = int(file.height)

    image = image.read()
    if type(image) != bytes:
        image = image.encode()
    sha1 = hashlib.sha1(image).hexdigest()

    return JsonResponse({'sha1': sha1, 'width': width, 'height': height, 'type': image_type, 'status': 200}, safe = False)

def handle_uploaded_file(f, user):
    with open('./image_files/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        image = user.imagedata_set.create(sha1=None, name=f.name, width=None, height=None, type=None)
