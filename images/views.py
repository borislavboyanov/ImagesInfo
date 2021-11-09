from django.shortcuts import render
from django.http import JsonResponse
from PIL import ImageFile
import hashlib
import requests
from .models import ImageData
# Create your views here.

def create(request):
    try:
        if 'http://' not in request.GET['url'] and 'https://' not in request.GET['url']:
            request.GET['url'] = 'http://' + request.GET['url']
        head = requests.head(request.GET['url'])
    except requests.exceptions.URLRequired:
        return JsonResponse(data = {'response': 'Sorry, the provided string is not a URL.'})
    except:
        return JsonResponse(data = {'response': 'Sorry, something went wrong.'})

    if 'image' not in head.headers['Content-Type']:
        return JsonResponse(data = {'response': 'Sorry, the provided link is not of an image.'})

    image = requests.get(request.GET['url']).content
    parser = ImageFile.Parser()
    parser.feed(image)

    sha1 = hashlib.sha1(image).hexdigest()

    image_type = head.headers["Content-Type"][6:]

    image_data = ImageData(sha1=sha1, width=parser.image.size[0], height=parser.image.size[1], type=image_type)
    image_data.save()

    return JsonResponse(data = {'response': 'Success!.'}, safe=False)
