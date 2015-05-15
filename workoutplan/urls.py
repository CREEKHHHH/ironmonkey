from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from nutrition.views import *
admin.autodiscover()
from nutrition.api.autocompleter import autocomplete,searchAPI
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'workoutplan.views.home', name='home'),
    # url(r'^workoutplan/', include('workoutplan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^home/',homePage),
    url(r'^browse/(?P<id>[-\d]+)',browse),
   url(r'^api/search/',searchAPI),
    url(r"^api/",autocomplete),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^replace/',replaceFoodItem),
    url(r'^',searchFoodItem),

)
