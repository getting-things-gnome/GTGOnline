# Create your views here.
import json

from django.http import HttpResponse

def resource_listing(request):
    #return HttpResponse('1', mimetype='application/json')
    return HttpResponse(json.dumps({
        "apiVersion": "1.0.0",
        "swaggerVersion": "1.2",
        "apis": [],
    }), mimetype='application/json')
