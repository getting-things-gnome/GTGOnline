# Create your views here.
import os
import json

from django.http import HttpResponse

def resource_listing(request):
    #return HttpResponse('1', mimetype='application/json')
    CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
    print "Current path = " + CURRENT_PATH
    json_data = open(CURRENT_PATH + '/resource.json')
    #data1 = json.load(json_data) // deserialises it
    #data2 = json.dumps(json_data)  #json formatted string
    resp = HttpResponse()
    resp['Access-Control-Allow-Origin'] = '*'
    resp['Access-Control-Max-Age'] = '120'
    resp['Access-Control-Allow-Credentials'] = 'true'
    resp['Access-Control-Allow-Methods'] = 'HEAD, GET, OPTIONS, POST, DELETE'
    resp['Access-Control-Allow-Headers'] = 'origin, content-type, accept, x-requested-with'
    resp['mimetype'] = 'application/json'
    resp.content = json_data
    return resp