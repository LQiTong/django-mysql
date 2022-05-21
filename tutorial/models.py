from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# _*_ coding:utf-8 _*_


# Create your models here.


class OutlookMail(models.Model):
    """微软邮箱"""
    mail = models.CharField(verbose_name='邮箱', max_length=255, default='')
    password = models.CharField(verbose_name='密码', max_length=255, default='')

    class Meta:
        verbose_name = '微软邮箱'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.password


class hotmail(models.Model):
    """微软邮箱"""
    mail = models.CharField(verbose_name='邮箱', max_length=255, default='')
    password = models.CharField(verbose_name='密码', max_length=255, default='')

    class Meta:
        verbose_name = '微软邮箱'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.password


class gmail(models.Model):
    """Gmail"""
    mail = models.CharField(verbose_name='邮箱', max_length=255, default='')
    password = models.CharField(verbose_name='密码', max_length=255, default='')

    class Meta:
        verbose_name = '谷歌邮箱'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.password


class net163(models.Model):
    """网易邮箱"""
    mail = models.CharField(verbose_name='邮箱', max_length=255, default='')
    password = models.CharField(verbose_name='密码', max_length=255, default='')

    class Meta:
        verbose_name = '网易邮箱'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.password