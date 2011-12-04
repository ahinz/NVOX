from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'nvox.views.home', name='home'),
    # url(r'^nvox/', include('nvox.foo.urls')),                       

    url(r'^$', 'nvox.voting.views.home'),
    url(r'^create$', 'nvox.voting.views.create'),
    url(r'^vote/up$', 'nvox.voting.views.vote_up'),
    url(r'^vote/down$', 'nvox.voting.views.vote_down'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
