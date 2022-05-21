from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.authhelper import get_signin_url, get_token_from_code, get_access_token
from tutorial.outlookservice import get_me, get_my_messages, get_my_events, get_my_contacts
from tutorial.outlook_pop3 import Outlook
import time
from .models import OutlookMail, hotmail, gmail, net163
import re
from bs4 import BeautifulSoup
import chardet

outlook = Outlook()
# password = 'lZpXpD026'

# 数据库数据
outlook_mail = OutlookMail.objects.all()  # outlook 邮箱
hotmail = hotmail.objects.all()  # hotmail 邮箱
gmail = gmail.objects.all()  # gmail 邮箱
net163 = net163.objects.all()  # 163 邮箱
# 测试链接
# print('hotmail --> ', hotmail)
# print('gmail --> ', gmail)
# print('net163 --> ', net163)


# 判断是何种类型邮箱
def matchPwd(username):
    if '@outlook' in username:
        password = f'{outlook_mail.filter(mail=username)[0]}'
        print('outlook password -->', password)
        outlook.login(username, password)
        inbox = outlook.select('Inbox')
        hasUnread = outlook.hasUnread()
        if hasUnread:
            latest_unread_mail = outlook.unread()
            decoded = outlook.mailbody()
            code = re.compile(r'\d{6}', re.S).findall(str(decoded))[0]
            mail_date = outlook.maildate()
            return {'mail': username, 'inbox': inbox, 'hasUnread': hasUnread, 'code': code, 'mail_date': mail_date}
        else:
            return {'mail': username, 'inbox': inbox, 'hasUnread': hasUnread, 'code': '--', 'mail_date': '--' }

    elif '@hotmail' in username:
        password = f'{hotmail.filter(mail=username)[0]}'
        print('hotmail password -->', password)
        outlook.login(username, password)
        inbox = outlook.select('Inbox')
        hasUnread = outlook.hasUnread()
        if hasUnread:
            latest_unread_mail = outlook.unread()
            decoded = outlook.mailbody()
            code = re.compile(r'\d{6}', re.S).findall(str(decoded))[0]
            mail_date = outlook.maildate()
            return {'mail': username, 'inbox': inbox, 'hasUnread': hasUnread, 'code': code, 'mail_date': mail_date}
        else:
            return {'mail': username, 'inbox': inbox, 'hasUnread': hasUnread, 'code': '--', 'mail_date': '--' }
    elif '@gmail' in username:
        password = f'{gmail.filter(mail=username)[0]}'
        print('password -->', password)
    elif '@163' in username:
        password = f'{net163.filter(mail=username)[0]}'
        print('password -->', password)
    else:
        password = f'{outlook_mail.filter(mail=username)[0]}'
        print('password -->', password)


# Create your views here.

def home(route):
    username = route.GET["mail"]
    app = route.GET["app"]
    # 数据库过滤匹配
    context = matchPwd(username)
    context['app'] = app
    print('context --> ', context)
    return render(route, 'tutorial/home.html', context)


def gettoken(route):
    auth_code = route.GET['code']
    redirect_uri = route.build_absolute_uri(reverse('tutorial:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    user = get_me(access_token)
    refresh_token = token['refresh_token']
    expires_in = token['expires_in']

    # expires_in is in seconds
    # Get current timestamp (seconds since Unix Epoch) and
    # add expires_in to get expiration time
    # Subtract 5 minutes to allow for clock differences
    expiration = int(time.time()) + expires_in - 300

    # Save the token in the session
    route.session['access_token'] = access_token
    route.session['refresh_token'] = refresh_token
    route.session['token_expires'] = expiration

    return HttpResponseRedirect(reverse('tutorial:mail'))


def mail(route):
    access_token = get_access_token(route, route.build_absolute_uri(reverse('tutorial:gettoken')))
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        messages = get_my_messages(access_token)
        context = {'messages': messages['value']}
        return render(route, 'tutorial/mail.html', context)


def events(route):
    access_token = get_access_token(route, route.build_absolute_uri(reverse('tutorial:gettoken')))
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        events = get_my_events(access_token)
        context = {'events': events['value']}
        return render(route, 'tutorial/events.html', context)


def contacts(route):
    access_token = get_access_token(route, route.build_absolute_uri(reverse('tutorial:gettoken')))
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('tutorial:home'))
    else:
        contacts = get_my_contacts(access_token)
        context = {'contacts': contacts['value']}
        return render(route, 'tutorial/contacts.html', context)
