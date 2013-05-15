from django.conf.urls import patterns, include, url
from api import views
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
router = DefaultRouter()
router.register(r'status', views.StatusViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = patterns('',
        url(r'^', include(router.urls)),

    # Examples:
    # url(r'^$', 'thalia.views.home', name='home'),
    # url(r'^thalia/', include('thalia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

)
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)
urlpatterns += patterns('',
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token')
)
