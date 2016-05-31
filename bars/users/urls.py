from django.conf.urls import url


from .views import (
    user_create,
    login,
    logout,
)


urlpatterns = [
    url(r'^user-create/$', user_create),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
]
