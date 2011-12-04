from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'nvox.views.home', name='home'),
    # url(r'^nvox/', include('nvox.foo.urls')),                       

    url(r'^$', 'nvox.voting.views.home'),
    url(r'^create$', 'nvox.voting.views.create'),
    url(r'^vote/up$', 'nvox.voting.views.vote_up'),
    url(r'^vote/down$', 'nvox.voting.views.vote_down'),

    url(r'^plogin$', 'nvox.voting.views.login_user'),
    url(r'^logout$', 'nvox.voting.views.logout'),

    url(r'^community/(?P<community_title>[A-Za-z0-9\-\s]+)$', 'nvox.voting.views.home_filter'),
    url(r'^info$', 'nvox.voting.views.home_info_index'),
    url(r'^community/(?P<community_title>[A-Za-z0-9\-\s]+)/info$', 'nvox.voting.views.home_info'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^comments/', include('django.contrib.comments.urls')),
)
