from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {"template_name": "Game/loginform.html"},
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'get-elements-by-category/(?P<category_id>[0-9]+)',
        views.element_list, name='get-elements-by-cat'),
    url (r'get_categories', views.get_catigories, name='get_categories')
    ]
