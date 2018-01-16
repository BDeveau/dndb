from django.conf.urls import include, url
from django.contrib import admin
import dndb.views
from django.contrib.auth import views as auth_views
admin.autodiscover()

# Examples:
# url(r'^$', 'core.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', dndb.views.index, name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^admin/', include(admin.site.urls), name='admin'),


    url(r'^register/$', dndb.views.register_user.as_view(), name='register'),

    url(r'^campaigns/$', dndb.views.campaigns.as_view(), name='campaigns'),
    url(r'^campaign/new/$', dndb.views.campaign_create.as_view(), name='campaign_create'),
    url(r'^campaign/(?P<campaign_id>[0-9]+)/$', dndb.views.overview, name='overview'),
    url(r'^campaign/(?P<pk>[0-9]+)/invite/$', dndb.views.campaign_invite.as_view(), name='invite'),
    url(r'^selectcampaign/(?P<campaign_id>[0-9]+)/$', dndb.views.selectcampaign, name='selectcampaign'),

    url(r'^profile/$', dndb.views.user_detail, name='profile'),
    url(r'^profile/password/$', dndb.views.change_password, name='password'),

    url(r'^campaign/(?P<campaign_id>[0-9]+)/locations/$', dndb.views.locations, name='locations'),
    url(r'^location/(?P<location_id>[0-9]+)/$', dndb.views.location_detail, name='location'),
    url(r'^location/new/$', dndb.views.location_create, name='location_create'),
    url(r'^location/(?P<location_name>[-\w\d\' ]+)/$', dndb.views.location_detail, name='locationByName'),
    url(r'^location/(?P<location_id>[0-9]+)/character/new/$', dndb.views.character_create, name='location_character_create'),
    url(r'^location/(?P<location_id>[0-9]+)/task/new/$', dndb.views.task_create, name='location_task_create'),
    url(r'^location/(?P<parent_id>[0-9]+)/location/new/$', dndb.views.location_create, name='location_location_create'),


    url(r'^campaign/(?P<campaign_id>[0-9]+)/characters/$', dndb.views.characters, name='characters'),
    url(r'^character/(?P<character_id>[0-9]+)/$', dndb.views.character_detail, name='character'),
    url(r'^character/new/$', dndb.views.character_create, name='character_create'),
    url(r'^character/(?P<character_name>[-\w\d\' ]+)/$', dndb.views.character_detail, name='characterByName'),
    url(r'^character/(?P<character_id>[0-9]+)/task/new/$', dndb.views.task_create, name='character_task_create'),

    url(r'^campaign/(?P<campaign_id>[0-9]+)/tasks/$', dndb.views.tasks, name='tasks'),
    url(r'^task/(?P<task_id>[0-9]+)/$', dndb.views.task_detail, name='task'),
    url(r'^task/(?P<task_name>[-\w\d\' ]+)/$', dndb.views.task_detail, name='taskByName'),
    url(r'^task/new/$', dndb.views.task_create, name='task_create'),

    url(r'^campaign/(?P<campaign_id>[0-9]+)/items/$', dndb.views.items, name='items'),
    url(r'^item/(?P<item_id>[0-9]+)/$', dndb.views.item_detail, name='item_detail'),
    url(r'^item/(?P<item_name>[-\w\d\' ]+)/$', dndb.views.item_detail, name='itemByName'),
    url(r'^item/new/$', dndb.views.item_create, name='item_create'),

    url(r'^post/(?P<post_id>[0-9]+)/$', dndb.views.post_detail, name='post_detail'),
    url(r'^post/edit/(?P<post_id>[0-9]+)/$', dndb.views.post_edit, name='post_edit'),
    url(r'^post/new/$', dndb.views.post_create, name='post_create'),

    url(r'^comment/(?P<comment_id>[0-9]+)/$', dndb.views.comment_detail, name='comment_detail'),
    url(r'^comment/new/$', dndb.views.comment_create, name='comment_create'),
]
