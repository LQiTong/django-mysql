from django.urls import path
from tutorial import views 

app_name = 'tutorial'
urlpatterns = [ 
  # The home view ('/tutorial/') 
  path('', views.home, name='home'),
  # Explicit home ('/tutorial/home/') 
  path('home/', views.home, name='home'),
  # Redirect to get token ('/tutorial/gettoken/')
  path('gettoken/', views.gettoken, name='gettoken'),
  # Mail view ('/tutorial/mail/')
  path('mail/', views.mail, name='mail'),
  # Events view ('/tutorial/events/')
  path('events/', views.events, name='events'),
  # Contacts view ('/tutorial/contacts/')
  path('contacts/', views.contacts, name='contacts'),
]
