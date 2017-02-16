from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import dndb.views
from django.contrib.auth import views as auth_views

# Examples:
# url(r'^$', 'core.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', dndb.views.index, name='index'),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^campaigns/', dndb.views.campaigns, name='campaigns'),
    url(r'^campaign/(?P<campaign_id>[0-9]+)/locations/', dndb.views.locations, name='locations'),
    url(r'^campaign/(?P<campaign_id>[0-9]+)/characters/', dndb.views.characters, name='characters'),
    url(r'^selectcampaign/(?P<campaign_id>[0-9]+)', dndb.views.selectcampaign, name='selectcampaign'),
]
