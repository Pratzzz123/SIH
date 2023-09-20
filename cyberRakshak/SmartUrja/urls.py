from django.contrib import admin
from django.urls import path
# from SmartUrja.views import main
from SmartUrja import views

urlpatterns = [
    path('', views.main, name = 'main'),
    path('submit', views.submit, name='submit'),
    path('submit', views.submit, name='submit'),
    # path('activate/<uidb64>/<token>', views.activate, name = 'activate')
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name = 'activate')

]
