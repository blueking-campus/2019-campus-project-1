# -*- coding: utf-8 -*-

# import from apps here


# import from lib
from django.db import models
from django.db.models.sql.aggregates import Count

from account.models import BkUser

STATUS_CHOICES = (
    (0, u'申报中'),
    (1, u'未通过'),
    (2, u'已通过'),
    (3, u'未获奖'),
    (4, u'已获奖'),
)


class UserInfo(models.Model):
    id = models.AutoField(verbose_name=u'用户QQ信息id', primary_key=True)
    auth_token = models.CharField(max_length=255, blank=True, default='', verbose_name=u'用户openId')
    qq = models.CharField(max_length=20, default='', verbose_name=u'用户QQ')
    objects = models.Manager()

    class Meta:
        verbose_name = u'用户QQ信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'id: %d' % self.id


class Permission(models.Model):
    id = models.AutoField(verbose_name=u'用户权限id', primary_key=True)
    name = models.CharField(max_length=20, default='', verbose_name=u'用户权限名称')
    objects = models.Manager()

    class Meta:
        verbose_name = u'用户权限'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'id: %d name: %s' % (self.id, self.name)


class UserPermission(models.Model):
    id = models.AutoField(verbose_name=u'用户权限code id', primary_key=True)
    qq = models.CharField(max_length=20, default='', verbose_name=u'用户QQ')
    permission = models.ForeignKey(Permission, verbose_name=u'用户权限', on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        verbose_name = u'用户权限code'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'id: %d' % self.id


class Choice(models.Model):
    id = models.AutoField(verbose_name=u'项目级别id', primary_key=True)
    name = models.CharField(max_length=20, verbose_name=u'项目级别')
    objects = models.Manager()

    class Meta:
        verbose_name = u'项目级别选项'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'id: %d name: %s' % (self.id, self.name)


class Organization(models.Model):
    id = models.AutoField(verbose_name=u'组织id', primary_key=True)
    name = models.CharField(default='', max_length=20, verbose_name=u'组织名称')
    principal = models.CharField(default='', max_length=20, verbose_name=u'负责人')
    users = models.TextField(verbose_name=u'用户')
    updater = models.ForeignKey(UserInfo, verbose_name=u'更新者', on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False, verbose_name=u'是否被删除')
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = u'组织'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'id: %d name: %s' % (self.id, self.name)

    @staticmethod
    def to_array(organization_list):
        return [{
            'id': organization.id,
            'name': organization.name,
            'principal': organization.principal,
            'users': organization.users,
            'updater': organization.updater,
            'updated_time': organization.updated_time.strftime("%Y-%m-%d %H:%M:%S")
        } for organization in organization_list]

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'principal': self.principal,
            'users': self.users,
            'updater': self.updater,
            'updated_time': self.created_time.strftime("%Y-%m-%d %H:%M:%S")}


class Award(models.Model):
    id = models.AutoField(verbose_name=u'奖项id', primary_key=True)
    name = models.CharField(default='', max_length=50, verbose_name=u'奖项名字')
    requirement = models.TextField(default='', verbose_name=u'评奖条件')
    organization = models.ForeignKey(Organization, verbose_name=u'所属组织', on_delete=models.CASCADE)
    level = models.ForeignKey(Choice, verbose_name=u'项目级别', on_delete=models.CASCADE)
    # True表示需要上传附件，False表示不需要上传附件
    has_extra_info = models.BooleanField(default=True, verbose_name=u'是否要求上传附件')
    # False表示过期，True表示生效
    status = models.BooleanField(default=True, verbose_name=u'状态')
    is_delete = models.BooleanField(default=False, verbose_name=u'是否被删除')
    submit_start_time = models.DateTimeField(verbose_name=u'开始日期')
    submit_end_time = models.DateTimeField(verbose_name=u'结束日期')
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = u'奖项'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'id: %d name: %s' % (self.id, self.name)

    @staticmethod
    def to_array(award_list):
        return [{
            'info': award,
            'count': Form.objects.filter(award=award).count(),
            'awarded_count': Form.objects.filter(award=award, status=4).count()
        } for award in award_list]

    @staticmethod
    def my_award(award_list, qq):
        # form_list = Form.objects.filter(creator__contains=qq)
        UNDECLARED = -1
        results = []
        for award in award_list:
            form = Form.objects.filter(creator__contains=qq, award=award).first()
            if form:
                form_status = form.status
                status_info = form.get_status_display
                created_time = form.created_time
                creator = form.creator
                form_id = form.form_id
            else:
                form_status = UNDECLARED
                status_info = u"未申报"
                created_time = ""
                creator = ""
                form_id = UNDECLARED
            data = {
                'id': award.id,
                'name': award.name,
                'organization': award.organization,
                'status': award.status,
                'form_status': form_status,
                'status_info': status_info,
                'created_time': created_time,
                'creator': creator,
                'form_id': form_id
            }
            results.append(data)

        return results


class Form(models.Model):
    form_id = models.AutoField(verbose_name=u'申请表id', primary_key=True)
    award = models.ForeignKey(Award, verbose_name=u'奖项', on_delete=models.CASCADE)
    creator = models.CharField(default='', max_length=200, verbose_name=u'申请者')
    info = models.TextField(default='', verbose_name=u'事迹介绍')
    extra_info = models.FileField(verbose_name=u'附件', null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name=u'状态')
    updater = models.CharField(blank=True, max_length=20, verbose_name=u'审批者')
    comment = models.TextField(verbose_name=u'评语', blank=True)
    created_time = models.DateTimeField(verbose_name=u'申请时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name=u'审批时间', auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = u'申请表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return 'id: %d' % self.id
