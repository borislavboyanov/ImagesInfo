from django.http import JsonResponse
import io
import json
from PIL import ImageFile
import hashlib
import svglib.svglib as svg
from .models import ImageData

def generate_image_data(image):
    file = svg.svg2rlg(image)
    print('FILEEEEEEEEEEEEEEE', file)
    if not hasattr(file, 'height'):
        parser = ImageFile.Parser()
        parser.feed(image)
        if hasattr(parser.image, 'format'):
            image_type = parser.image.format.lower()
            width, height = parser.image.size
        else:
            return JsonResponse({'response': 'Sorry, the provided link is not of an image.', 'status': 400}, safe = False)
    else:
        image_type = 'svg'
        width = int(file.width)
        height = int(file.height)

    image = image.read()
    if type(image) != bytes:
        print('TYPEEEEEEE', type(image))
        image = image.encode()
    sha1 = hashlib.sha1(image).hexdigest()

    return JsonResponse({'sha1': sha1, 'width': width, 'height': height, 'type': image_type, 'status': 200}, safe = False)

def handle_uploaded_file(f, user):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        image = ImageData(sha1=None, name=f.name, width=None, height=None, type=None, user=user)
        image.save()
