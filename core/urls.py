from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import dndb.views

# Examples:
# url(r'^$', 'core.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', dndb.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^locations/', dndb.views.locations, name='locations')
    #url(r'^characters/', dndb.views.characters, name="characters")
]
