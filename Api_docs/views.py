# Create your views here.
from os import path
import json

from django.http import HttpResponse
from django.template import loader, RequestContext

def load_api_docs(request):
    template = loader.get_template('api_docs.html')
    context = RequestContext(request, {})
    resp = HttpResponse(template.render(context))
    return get_httpresponse_with_access_control(resp)

def resource_listing(request):
    JSON_FILE = '../GTGOnline/api_docs/resource.json'
    content = read_json_file(JSON_FILE)
    resp = HttpResponse(content, mimetype="application/json",)
    return get_httpresponse_with_access_control(resp)

def user_api(request):
    JSON_FILE = '../GTGOnline/api_docs/user_api.json'
    content = read_json_file(JSON_FILE)
    resp = HttpResponse(content, mimetype="application/json",)
    return get_httpresponse_with_access_control(resp)

def tasks_api(request):
    JSON_FILE = '../GTGOnline/api_docs/tasks_api.json'
    content = read_json_file(JSON_FILE)
    resp = HttpResponse(content, mimetype="application/json",)
    return get_httpresponse_with_access_control(resp)

def tags_api(request):
    JSON_FILE = '../GTGOnline/api_docs/tags_api.json'
    content = read_json_file(JSON_FILE)
    resp = HttpResponse(content, mimetype="application/json",)
    return get_httpresponse_with_access_control(resp)

def get_httpresponse_with_access_control(resp):
    resp['Access-Control-Allow-Origin'] = '*'
    resp['Access-Control-Max-Age'] = '120'
    resp['Access-Control-Allow-Credentials'] = 'true'
    resp['Access-Control-Allow-Methods'] = 'HEAD, GET, OPTIONS, POST, DELETE'
    resp['Access-Control-Allow-Headers'] = 'origin, content-type, ' + \
                                           'accept, x-requested-with'
    return resp

def read_json_file(file_relative_path):
    CURRENT_PATH = path.dirname(path.realpath(__file__))
    JSON_FILE = path.join(CURRENT_PATH, file_relative_path)
    json_data = open(JSON_FILE)
    json_loaded = json.loads(json_data.read())
    return json.dumps(json_loaded, indent=4)
