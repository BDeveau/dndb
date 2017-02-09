from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from dndb import views

# Examples:
# url(r'^$', 'core.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^locations/', views.locations, name="locations")
    url(r'^characters/', views.characters, name="characters")
]
