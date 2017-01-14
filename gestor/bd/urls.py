from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^acta/(?P<evaluacion>[0-9])/$', views.acta_evaluacion, name='acta'),
    url(r'^estadisticas/(?P<evaluacion>[0-9])/$', views.estadisticas_evaluacion, name='estadisticas'),
]