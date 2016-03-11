from django.shortcuts import render_to_response
from django.template import RequestContext


def list(request):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))


def edit(request, id):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))


def delete(request, id):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))


def detail(request, id):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))
