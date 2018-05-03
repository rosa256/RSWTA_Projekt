from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.oferta_list, name='oferta_list'), #oferta_list jest defaultowo włączana jako strona głowna
    url(r'^oferta/$', views.oferta_list, name='oferta_list'),
    url(r'^oferta/(?P<pk>\d+)/$', views.oferta_detail, name='oferta_detail'),
    url(r'^firma/$', views.firma_list, name='firma_list'),
    url(r'^firma/(?P<pk>\d+)/$', views.firma_detail, name='firma_detail'),
    url(r'^aplikant/$', views.aplikant_list, name='aplikant_list'),
    url(r'^aplikant/(?P<pk>\d+)/$', views.aplikant_detail, name='aplikant_detail'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^register/success$', views.register_success, name='register_success'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
]