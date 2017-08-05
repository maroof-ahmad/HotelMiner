from django.conf.urls import url
from django.views.generic import RedirectView

from HotelMiner import views

urlpatterns = [
    url('^$', views.index, name='home'),
]