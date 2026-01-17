from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='main-index'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('asct/', include('asct.urls')),
    path('docs/', include('docs.urls')),
    path('apps/blog/', include('blog.urls')),
    path('apps/polls/', include('polls.urls')),
    path('apps/events/', include('events.urls')),
    path('apps/echop/', include('eshop.urls')),
    # path('apps/library/', include('library.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = "ASCTool" # H1 헤더 및 로그인 양식 상단 텍스트
admin.site.site_title = "Automated System Check Tool" # 브라우저 페이지 <title> 태그 접미사
admin.site.index_title = "관리자 대시보드에 오신 것을 환영합니다" 