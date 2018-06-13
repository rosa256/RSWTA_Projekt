from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.oferta_list, name='oferta_list'), #oferta_list jest defaultowo włączana jako strona głowna
    url(r'^oferta/$', views.oferta_list, name='oferta_list'),
    url(r'^oferta/(?P<pk>\d+)/$', views.oferta_detail, name='oferta_detail'),
    url(r'^oferta/f=branza$', views.oferta_list_filter_branza, name='oferta_list_filter_branza'),
    url(r'^oferta/f=wakat$', views.oferta_list_filter_wakat, name='oferta_list_filter_wakat'),
    url(r'^oferta/f=lokalizacja$', views.oferta_list_filter_lokalizacja, name='oferta_list_filter_lokalizacja'),
    url(r'^oferta/f=wynagrodzenie$', views.oferta_list_filter_wynagrodzenie, name='oferta_list_filter_wynagrodzenie'),
    url(r'^firma/$', views.firma_list, name='firma_list'),
    url(r'^firma/(?P<pk>\d+)/$', views.firma_detail, name='firma_detail'),
    url(r'^firma/f=nazwa_firmy$', views.firma_list_filter_nazwa_firmy, name='firma_list_filter_nazwa_firmy'),
    url(r'^firma/f=miasto$', views.firma_list_filter_miasto, name='firma_list_filter_miasto'),

    url(r'^aplikant/$', views.aplikant_list, name='aplikant_list'),
    url(r'^aplikant/f=wiek$', views.aplikant_list_filter_wiek, name='aplikant_list_filter_wiek'),
    url(r'^aplikant/f=imie$', views.aplikant_list_filter_imie, name='aplikant_list_filter_imie'),
    url(r'^aplikant/f=wyksztalcenie$', views.aplikant_list_filter_wyksztalcenie, name='aplikant_list_filter_wyksztalcenie'),
    url(r'^aplikant/(?P<pk>\d+)/$', views.aplikant_detail, name='aplikant_detail'),


    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^register/success$', views.register_success, name='register_success'),
    url(r'^upload/success$', views.upload_success, name='upload_success'),
    url(r'^aplication/success$', views.aplication_success, name='aplication_success'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^update/(?P<pk>\d+)/$', views.edit_user, name='account_update'),

    url(r'^add/oferta/$', views.add_oferta, name='add_oferta'),
    url(r'^edit/oferts/(?P<pk>\d+)/$', views.edit_oferts, name='edit_oferts'),
    url(r'^aplications/$', views.show_aplications, name='show_aplications'),

    url(r'^upload_cv/$', views.upload_cv, name='upload_cv'),
    url(r'^aplication/$', views.add_aplication,name='add_aplication'),

    url(r'^captcha/', include('captcha.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)