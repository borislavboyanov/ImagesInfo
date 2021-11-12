from django.http import JsonResponse
import io
import json
from PIL import ImageFile
import hashlib
import svglib.svglib as svg
from .models import ImageData

def generate_image_data(image):
    file = svg.load_svg_file(image)
    if file == None:
        parser = ImageFile.Parser()
        parser.feed(image)
        if hasattr(parser.image, 'format'):
            image_type = parser.image.format.lower()
            width, height = parser.image.size
        else:
            return JsonResponse(json.dumps({'response': 'Sorry, the provided link is not of an image.'}), safe = False)
    else:
        image_type = 'svg'
        drawing = svg.svg2rlg(fake_file)
        print('WIDTH:', drawing)
        width = int(drawing.width)
        height = int(drawing.height)

    sha1 = hashlib.sha1(image).hexdigest()

    return JsonResponse({'sha1': sha1, 'width': width, 'height': height, 'type': image_type}, safe = False)

def handle_uploaded_file(f, user):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        image = ImageData(sha1=None, name=f.name, width=None, height=None, type=None, user=user)
        image.save()
