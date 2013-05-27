# Create your views here.

import json

from django.http import HttpResponse

from Tag_backend.tag import get_tags_by_user

def get_all_tags(request):
    tags = get_tags_by_user(request.user)
    return HttpResponse(json.dumps(tags, indent=4), \
                        mimetype="application/json")
