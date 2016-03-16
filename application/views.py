from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required

from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django_mailbox.models import Message
from application.models import Application, Vote
import re
from bs4 import BeautifulSoup
from datetime import datetime


def add_to_application(msg):
    parsed_html = BeautifulSoup(msg.html, 'html.parser')
    result = []
    for data in parsed_html.find_all('p'):
        result.append(data.text)

    tel = [x for x in result if 'เบอร์โทรศัพท์ :' in x]
    tel = tel[0][tel[0].index(':') + 1:].strip().replace('-', '')

    mail = [x for x in result if 'mail' in x]
    mail = mail[0][mail[0].index(':') + 1:].strip()

    university = [x for x in result if 'มหาวิทยาลัย :' in x]
    university = university[0][university[0].index(':') + 1:].strip()

    major = [x for x in result if 'คณะและสาขา :' in x]
    major = major[0][major[0].index(':') + 1:].strip()

    start_date = [
        x for x in result if 'วันที่สามารถเริ่มฝึกงานได้ (mm/dd/yyyy) :' in x]
    start_date = start_date[0][start_date[0].index(':') + 1:].strip()
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

    end_date = [
        x for x in result if 'วันที่ที่สิ้นสุดการฝึกงาน (mm/dd/yyyy) :' in x]
    end_date = end_date[0][end_date[0].index(':') + 1:].strip()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    semester_year = [x for x in result if 'ชั้นปี :' in x]
    semester_year = semester_year[0][semester_year[0].index(':') + 1:].strip()

    gpa = [x for x in result if 'GPA :' in x]
    gpa = gpa[0][gpa[0].index(':') + 1:].strip()

    # company = ",".join([x for x in result if 'บริษัทที่สนใจ :' in x])
    company = ','.join(re.findall(
        r'(CodeApp|Fire One One|RGB72|Fiveloop|Cookly|Aksorn|Sellsuki|Wongnai|ClaimDi|Bento|Vetside|Peak Engine|Ascend Group)', msg.text))

    try:
        app, created = Application.objects.get_or_create(
            message_id=msg.message_id)
        if created:
            app.name = msg.subject[msg.subject.index(':') + 1:].strip()
            app.content = msg.html
            app.position = ','.join(re.findall(
                r'(Software Engineer|QA Automation Engineer|Digital Marketing|Product Owner|Graphic Designer|UX Designer|Sale|Business|Designer|Developer|QA / Tester)', msg.subject))

            app.tel = tel
            app.email = mail
            app.university = university
            app.major = major
            app.semester_year = result[7][result[7].index(':') + 1].strip()
            app.gpa = gpa
    #         app.interest = result[9][result[9].index(':') + 1].strip()
            app.company = company
    #         app.intern_type = result[11][result[11].index(':') + 1].strip()
            app.start_date = start_date
            app.end_date = end_date

    #         app.award = result[15][result[15].index(':') + 1].strip()

    #         # สำหรับ Development และ QA เท่านั้น
    #         app.technical_skills = result[16][
    #             result[16].index(':') + 1].strip()
    #         app.dev_what_you_want_to_learn = result[
    #             17][result[17].index(':') + 1].strip()
    #         app.dev_exp = result[18][result[18].index(':') + 1].strip()
    # app.dev_short_blub = result[19][result[19].index(':') + 1].strip()

    #         # สำหรับ Graphic เท่านั้น
    #         app.design_design_software = result[20][
    #             result[20].index(':') + 1].strip()
    #         app.design_portfolio = result[21][
    #             result[21].index(':') + 1].strip()

    #         # สำหรับ Product Owner เท่านั้น
    #         app.po_platform_tools = result[22][
    #             result[22].index(':') + 1].strip()
    #         app.po_fav_startup = result[22][result[22].index(':') + 1].strip()
    #         app.po_biz_idea = result[23][result[23].index(':') + 1].strip()
    #         app.po_short_blub = result[24][result[24].index(':') + 1].strip()
    #         app.po_more_interesting = result[25][
    #             result[25].index(':') + 1].strip()

    #         # สำหรับ Sale / Business เท่านั้น
    #         app.mkt_advertising_platforms_or_marketing_tools = result[
    #             26][result[26].index(':') + 1].strip()
    #         app.mkt_short_blub = result[27][result[27].index(':') + 1].strip()
    #         app.mkt_fav_brand = result[28][result[28].index(':') + 1].strip()
            app.save()
    # # except IntegrityError:
    # #     print("IntegrityError : %s" % msg.subject)
    except ValueError:
        print("ValueError : %s" % msg.subject)


@permission_required('application.can_process', raise_exception=True)
@login_required
def process_new_application(request):
    for msg in Message.objects.all():
        add_to_application(msg)
    return redirect(reverse('application_home_urls'))


@permission_required('application.can_list', raise_exception=True)
@login_required
def list(request):
    application_list = Application.objects.all()
    paginator = Paginator(application_list, 30)
    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    return render_to_response('application_list.html',
                              {'applications': applications},
                              context_instance=RequestContext(request))


@permission_required('application.can_review', raise_exception=True)
@login_required
def application_review(request):
    cat = request.GET.get("cat")
    page = request.GET.get('page')
    application_list = Application.objects.filter(position__contains=cat)
    paginator = Paginator(application_list, 1)

    querystring = '?'
    querystring += 'cat=%s&' % cat if cat else ''
    querystring += 'page=%s&' % page if page else ''
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    return render_to_response('application_review.html',
                              {
                                  'applications': applications,
                                  'next': querystring
                              },
                              context_instance=RequestContext(request))


@permission_required('application.can_edit', raise_exception=True)
@login_required
def edit(request, id):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))


@permission_required('application.can_delete', raise_exception=True)
@login_required
def delete(request, id):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))


@permission_required('application.can_see_detail', raise_exception=True)
@login_required
def detail(request, id):
    result = {}
    return render_to_response('index.html',
                              result,
                              context_instance=RequestContext(request))


@permission_required('application.can_vote', raise_exception=True)
@login_required
def vote(request, id, score):
    app = get_object_or_404(Application, id=id)
    vote, created = Vote.objects.get_or_create(
        application=app, user=request.user, match=1, defaults={'point': score})
    vote.point = score
    vote.save()
    cat = request.GET.get("cat")
    page = request.GET.get('page')
    querystring = '?'
    querystring += 'cat=%s&' % cat if cat else ''
    querystring += 'page=%s&' % page if page else ''
    return redirect(
        reverse('application_review_urls') + querystring)
