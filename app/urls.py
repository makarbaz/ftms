from django.urls import path
from .import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('',views.loginpage, name='login'),
    path('send/',views.send_message, name='send_message'),
    path('messages/',views.read_message, name='read_message'),
    path('inbox/',views.inbox, name='inbox'),
    path("logout/",views.logout,name="logout"),
    path('tracker/',views.tracker, name='tracker'),
    path('app/',views.generate_application_number, name='generate_application_number')
   
]