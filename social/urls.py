from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import user_detail, user_detail_view

urlpatterns = [
    url(r'^', include("posts.urls", namespace="posts")),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('friendship.urls')),
    url(r'^user/(?P<u>[\w.@+-]+)/$', user_detail, name="user_detail"),
    url(r'^profile/$', user_detail_view, name="profile")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
