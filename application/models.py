from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Application(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    name = models.CharField(max_length=250)
    tel = models.CharField(max_length=250)
    email = models.CharField(max_length=250)

    university = models.CharField(max_length=250, null=True, blank=True)
    major = models.CharField(max_length=250, null=True, blank=True)
    semester_year = models.CharField(max_length=250, null=True, blank=True)
    gpa = models.DecimalField(
        decimal_places=2, max_digits=3, null=True, blank=True)

    interest = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=250, null=True, blank=True)
    intern_type = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=250, null=True, blank=True)

    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=True)

    award = models.TextField(null=True, blank=True)

    # สำหรับ Development และ QA เท่านั้น
    technical_skills = models.TextField(null=True, blank=True)
    dev_what_you_want_to_learn = models.TextField(null=True, blank=True)
    dev_exp = models.TextField(null=True, blank=True)
    dev_short_blub = models.TextField(null=True, blank=True)

    # สำหรับ Graphic เท่านั้น
    design_design_software = models.TextField(null=True, blank=True)
    design_portfolio = models.TextField(null=True, blank=True)

    # สำหรับ Product Owner เท่านั้น
    po_platform_tools = models.TextField(null=True, blank=True)
    po_fav_startup = models.TextField(null=True, blank=True)
    po_biz_idea = models.TextField(null=True, blank=True)
    po_short_blub = models.TextField(null=True, blank=True)
    po_more_interesting = models.TextField(null=True, blank=True)

    # สำหรับ Sale / Business เท่านั้น
    mkt_advertising_platforms_or_marketing_tools = models.TextField(
        null=True, blank=True)
    mkt_short_blub = models.TextField(null=True, blank=True)
    mkt_fav_brand = models.TextField(null=True, blank=True)

    message_id = models.CharField(max_length=250)

    def get_content(self):
        return self.content[(self.content.index('GPA') + 20):(self.content.index('--') - 3)]

    def __str__(self):
        return self.name

    def get_vote(self):

        return "%s" % (
            # self.vote_set.aggregate(avg=Avg('point'))['avg'],
            self.vote_set.count()
        )

    def get_avg(self):
        return self.vote_set.aggregate(avg=Avg('point'))['avg']

    def is_voted(self):
        return self.vote_set

    def get_vote_list(self):
        return self.vote_set.all()

    class meta:
        ordering = ['create_date']


class Vote(models.Model):
    application = models.ForeignKey(Application)
    user = models.ForeignKey(User)
    match = models.IntegerField()
    point = models.IntegerField()

    class meta:
        unique_together = ('application', 'user', 'match')
