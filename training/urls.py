from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:catalog_id>/', views.artwork_detail, name='artwork_detail'),
    path('phase/<int:number>/', views.phase_detail, name='phase_detail'),
    path('program/', views.program, name='program'),
    path('session/start/', views.session_start, name='session_start'),
    path('session/start/<str:catalog_id>/', views.session_start_artwork, name='session_start_artwork'),
    path('session/<int:pk>/view/', views.session_view, name='session_view'),
    path('session/<int:pk>/assess/', views.session_assess, name='session_assess'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
    path('sessions/', views.session_log, name='session_log'),
    path('image-streaming/', views.image_streaming, name='image_streaming'),
    path('captures/', views.capture_list, name='capture_list'),
    path('captures/new/', views.capture_new, name='capture_new'),
    path('progress/', views.progress, name='progress'),
    path('vviq/', views.vviq, name='vviq'),
    path('settings/', views.settings_view, name='settings'),
    path('api/session/<int:pk>/update-timing/', views.api_update_timing, name='api_update_timing'),
    path('api/progress-data/', views.api_progress_data, name='api_progress_data'),
]
