from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django_mailbox.models import Message


@permission_required('application.can_list')
def list(request):
    result = {
        'applications': Message.objects.all()
    }
    return render_to_response('application_list.html',
                              result,
                              context_instance=RequestContext(request))


@permission_required('application.can_edit')
def edit(request, id):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))


@permission_required('application.can_delete')
def delete(request, id):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))


@permission_required('application.can_see_detail')
def detail(request, id):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))
