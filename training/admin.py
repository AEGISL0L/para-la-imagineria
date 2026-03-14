from django.contrib import admin
from .models import (
    BrainArea, Phase, TrainingMethod, Artwork,
    UserProfile, TrainingSession, FieldCapture, VVIQResponse,
)


@admin.register(BrainArea)
class BrainAreaAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('number', 'title')
    filter_horizontal = ('primary_circuits',)


@admin.register(TrainingMethod)
class TrainingMethodAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'implementable_in_app')


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('catalog_id', 'artist', 'title', 'phase', 'emotional_category', 'order_standard')
    list_filter = ('phase', 'emotional_category')
    search_fields = ('catalog_id', 'artist', 'title')
    filter_horizontal = ('brain_areas',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('mode', 'program_start_date', 'current_phase')


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'artwork', 'session_type', 'date', 'vividness_rating')
    list_filter = ('session_type', 'date')


@admin.register(FieldCapture)
class FieldCaptureAdmin(admin.ModelAdmin):
    list_display = ('capture_type', 'quality', 'date', 'eyes_open', 'deliberate')
    list_filter = ('capture_type', 'eyes_open')


@admin.register(VVIQResponse)
class VVIQResponseAdmin(admin.ModelAdmin):
    list_display = ('total_score', 'date', 'context')
