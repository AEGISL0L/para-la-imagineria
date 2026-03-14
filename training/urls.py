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

    # Symbols
    path('symbols/', views.symbol_list, name='symbol_list'),
    path('symbols/new/', views.symbol_create, name='symbol_create'),
    path('symbols/<int:pk>/edit/', views.symbol_edit, name='symbol_edit'),
    path('symbols/<int:pk>/delete/', views.symbol_delete, name='symbol_delete'),
    path('symbols/<int:pk>/confirm-delete/', views.symbol_confirm_delete, name='symbol_confirm_delete'),

    # Workspace
    path('workspace/', views.workspace_start, name='workspace_start'),
    path('workspace/<int:pk>/exercise/', views.workspace_exercise, name='workspace_exercise'),
    path('workspace/<int:pk>/assess/', views.workspace_assess, name='workspace_assess'),
    path('workspace/<int:pk>/', views.workspace_detail, name='workspace_detail'),
    path('workspace/log/', views.workspace_log, name='workspace_log'),

    # Capabilities
    path('capabilities/', views.capability_map, name='capability_map'),
    path('api/capability/<int:pk>/update/', views.api_capability_update, name='api_capability_update'),
]
