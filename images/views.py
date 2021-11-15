from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
import json
import random
import re
import requests
import uuid
from .action_controller import generate_image_data, handle_uploaded_file, NotAnImage
from .models import ImageData
from .models import User
# Create your views here.



@csrf_exempt
def create(request):
    url = request.POST['url']
    try:
        if 'http://' not in url and 'https://' not in url:
            url = 'http://' + url
        head = requests.head(url)
        if 'image' not in head.headers['Content-Type']:
            raise NotAnImage
    except requests.exceptions.URLRequired:
        return JsonResponse({'response': 'Sorry, the provided string is not a URL.', 'status': 400}, safe = False)
    except NotAnImage as e:
        return JsonResponse({'response': e.message, 'status': 400}, safe = False)
    except:
        return JsonResponse({'response': 'Sorry, something went wrong.', 'status': 400}, safe = False)

    image = requests.get(url).content
    fake_file = io.BytesIO(image)

    data = json.loads(generate_image_data(fake_file).content)
    image_data = ImageData(sha1=data['sha1'], name=None, width=data['width'], height=data['height'], type=data['type'], user=None)
    image_data.save()

    return JsonResponse({'response': 'Success', 'status': 200}, safe = False)

@csrf_exempt
def upload_images(request):
    image_formats = ('jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'svg', 'ppm', 'pgm', 'pbm', 'pnm')
    files = request.FILES.getlist('files')
    for index, f in enumerate(files):
        if f.name.split('.')[-1] not in image_formats or len(f.name.split('.')) == 1:
            #return JsonResponse({'Error': 'One or more of the uploaded files is not an image.'}, safe = False)
            del files[index]
    user = User(url = uuid.uuid1(random.randint(0, 2**48 - 1)))
    user.save()
    for f in files:
        handle_uploaded_file(f, user)

    return JsonResponse({'url': 'http://localhost:8000/check/' + str(user.url), 'status': 200}, safe = False)

def check_images(request, url):
    try:
        user = User.objects.get(url=url)
    except:
        return JsonResponse({'response': "This URL doesn't exist!", 'status': 400}, safe = False)

    for image in user.imagedata_set.all():
        if image.sha1 == None:
            return JsonResponse({'response': "Your images are not ready. Please, come again later.", 'status': 200}, safe = False)

    images = json.loads(serializers.serialize('json', user.imagedata_set.all()))
    for index, image in enumerate(images):
        images[index] = image['fields']
    return JsonResponse(images, safe = False)
