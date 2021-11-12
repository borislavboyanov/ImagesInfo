from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
import json
import re
import requests
import uuid
from .action_controller import generate_image_data, handle_uploaded_file
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
    except requests.exceptions.URLRequired:
        return JsonResponse(json.dumps({'response': 'Sorry, the provided string is not a URL.'}), safe = False)
    except:
        return JsonResponse(json.dumps({'response': 'Sorry, something went wrong.'}), safe = False)

    image = requests.get(url).content

    data = json.loads(generate_image_data(image).content)
    image_data = ImageData(sha1=data['sha1'], name=None, width=data['width'], height=data['height'], type=data['type'], user=None)
    image_data.save()

    return JsonResponse(json.dumps({'response': 'Success'}), safe = False)

@csrf_exempt
def upload_images(request):
    image_formats = ('jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'svg', 'ppm', 'pgm', 'pbm', 'pnm')
    files = request.FILES.getlist('files')
    for f in files:
        if f.name.split('.')[-1] not in image_formats or len(f.name.split('.')) == 1:
            return JsonResponse(json.dumps({'Error': 'One or more of the uploaded files is not an image.'}), safe = False)
    user = User(url = uuid.uuid1(random.randint(0, 2**48 - 1)))
    user.save()
    for f in files:
        handle_uploaded_file(f, user)

    return JsonResponse(json.dumps({'url': 'http://localhost/' + user.url}))

def check_images(request):
    try:
        user = User.objects.get(url=request.GET['url'])
    except:
        return JsonResponse(json.dumps({'response': "This URL doesn't exist!"}), safe = False)

    for image in user.imagedata_set.all():
        if image.sha1 == None:
            return JsonResponse(json.dumps({'response': "Your images are not ready. Please, come again later."}), safe = False)
    return JsonResponse(json.dumps(user.imagedata_set.all()), safe = False)