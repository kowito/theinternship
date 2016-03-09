from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))
