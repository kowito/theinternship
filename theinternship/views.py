from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))


def profile(request):
    result = {'user': request.user}
    return render_to_response('profile.html',
                              result,
                              context_instance=RequestContext(request))
