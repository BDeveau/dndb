from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import dndb.views

# Examples:
# url(r'^$', 'core.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', dndb.views.index, name='index'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^campaigns/', dndb.views.campaigns, name='campaigns'),
    url(r'^campaign/(?P<campaign_id>[0-9]+)/locations/', dndb.views.locations, name='locations'),
    url(r'^campaign/(?P<campaign_id>[0-9]+)/characters/', dndb.views.characters, name='characters'),
]
