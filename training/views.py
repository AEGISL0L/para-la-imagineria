import json
from datetime import timedelta

from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    FieldCaptureForm, SessionAssessForm,
    UserProfileForm, VVIQForm,
)
from .models import (
    Artwork, FieldCapture, Phase, TrainingMethod, TrainingSession,
    UserProfile, VVIQResponse,
)


def dashboard(request):
    profile = UserProfile.get_instance()
    recent_sessions = TrainingSession.objects.select_related('artwork', 'artwork__phase')[:5]
    recent_captures = FieldCapture.objects.all()[:5]
    total_sessions = TrainingSession.objects.count()
    phases = Phase.objects.prefetch_related('artworks')

    avg_ratings = TrainingSession.objects.filter(
        vividness_rating__isnull=False
    ).aggregate(
        avg_vividness=Avg('vividness_rating'),
        avg_stability=Avg('stability_rating'),
        avg_detail=Avg('detail_rating'),
    )

    current_week = None
    if profile.program_start_date:
        delta = (timezone.now().date() - profile.program_start_date).days
        current_week = min(delta // 7 + 1, 8)

    return render(request, 'training/dashboard.html', {
        'recent_sessions': recent_sessions,
        'recent_captures': recent_captures,
        'total_sessions': total_sessions,
        'phases': phases,
        'avg_ratings': avg_ratings,
        'current_week': current_week,
    })


def catalog(request):
    profile = UserProfile.get_instance()
    artworks = Artwork.objects.select_related('phase').prefetch_related('brain_areas')

    phase_filter = request.GET.get('phase')
    category_filter = request.GET.get('category')

    if phase_filter:
        artworks = artworks.filter(phase__number=phase_filter)
    if category_filter:
        artworks = artworks.filter(emotional_category=category_filter)

    if profile.mode == 'flat_affect':
        artworks = artworks.order_by('phase__number', 'order_flat_affect', 'order_standard')
    else:
        artworks = artworks.order_by('phase__number', 'order_standard')

    phases = Phase.objects.all()
    return render(request, 'training/catalog.html', {
        'artworks': artworks,
        'phases': phases,
        'phase_filter': phase_filter,
        'category_filter': category_filter,
    })


def artwork_detail(request, catalog_id):
    artwork = get_object_or_404(
        Artwork.objects.select_related('phase').prefetch_related('brain_areas'),
        catalog_id=catalog_id,
    )
    sessions = artwork.sessions.all()[:10]
    profile = UserProfile.get_instance()
    return render(request, 'training/artwork_detail.html', {
        'artwork': artwork,
        'sessions': sessions,
        'is_flat_affect': profile.mode == 'flat_affect',
    })


def phase_detail(request, number):
    phase = get_object_or_404(Phase.objects.prefetch_related('artworks', 'primary_circuits'), number=number)
    profile = UserProfile.get_instance()
    artworks = phase.artworks.prefetch_related('brain_areas')
    if profile.mode == 'flat_affect':
        artworks = artworks.order_by('order_flat_affect', 'order_standard')
    else:
        artworks = artworks.order_by('order_standard')
    methods = TrainingMethod.objects.all()
    return render(request, 'training/phase_detail.html', {
        'phase': phase,
        'artworks': artworks,
        'methods': methods,
        'is_flat_affect': profile.mode == 'flat_affect',
    })


def program(request):
    profile = UserProfile.get_instance()
    phases = Phase.objects.prefetch_related('artworks')

    week_phases = {
        1: (1, "Formas planas (Malevich, Albers)"),
        2: (2, "Patrones y movimiento (Riley, Escher)"),
        3: (3, "Objetos 3D aislados (Zurbarán, Morandi)"),
        4: (4, "Espacios con profundidad (Hopper, De Chirico)"),
        5: (5, "Formas orgánicas (Hokusai, O'Keeffe)"),
        6: (5, "Formas orgánicas — consolidación"),
        7: (6, "Escenas completas (Vermeer, Turner)"),
        8: (6, "Escenas completas — integración final"),
    }

    current_week = None
    if profile.program_start_date:
        delta = (timezone.now().date() - profile.program_start_date).days
        current_week = min(max(delta // 7 + 1, 1), 8)

    weeks = []
    for week_num in range(1, 9):
        phase_num, desc = week_phases[week_num]
        week_start = None
        if profile.program_start_date:
            week_start = profile.program_start_date + timedelta(weeks=week_num - 1)

        session_count = 0
        if week_start:
            week_end = week_start + timedelta(days=7)
            session_count = TrainingSession.objects.filter(
                date__date__gte=week_start, date__date__lt=week_end
            ).count()

        weeks.append({
            'number': week_num,
            'phase_number': phase_num,
            'description': desc,
            'start_date': week_start,
            'session_count': session_count,
            'is_current': current_week == week_num,
        })

    return render(request, 'training/program.html', {
        'weeks': weeks,
        'current_week': current_week,
        'phases': phases,
    })


def session_start(request):
    profile = UserProfile.get_instance()
    artworks = Artwork.objects.select_related('phase').all()
    if profile.mode == 'flat_affect':
        artworks = artworks.order_by('phase__number', 'order_flat_affect', 'order_standard')
    else:
        artworks = artworks.order_by('phase__number', 'order_standard')
    phases = Phase.objects.all()
    return render(request, 'training/session_start.html', {
        'artworks': artworks,
        'phases': phases,
    })


def session_start_artwork(request, catalog_id):
    artwork = get_object_or_404(Artwork, catalog_id=catalog_id)

    if request.method == 'POST':
        viewing_duration = int(request.POST.get('viewing_duration', 60))
        session = TrainingSession.objects.create(
            artwork=artwork,
            session_type='standard',
            viewing_duration=viewing_duration,
        )
        return redirect('training:session_view', pk=session.pk)

    return render(request, 'training/session_start_artwork.html', {
        'artwork': artwork,
    })


def session_view(request, pk):
    session = get_object_or_404(
        TrainingSession.objects.select_related('artwork', 'artwork__phase'),
        pk=pk,
    )
    profile = UserProfile.get_instance()
    return render(request, 'training/session_view.html', {
        'session': session,
        'is_flat_affect': profile.mode == 'flat_affect',
    })


def session_assess(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    profile = UserProfile.get_instance()

    if request.method == 'POST':
        form = SessionAssessForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('training:session_detail', pk=session.pk)
    else:
        form = SessionAssessForm(instance=session)

    return render(request, 'training/session_assess.html', {
        'session': session,
        'form': form,
        'is_flat_affect': profile.mode == 'flat_affect',
    })


def session_detail(request, pk):
    session = get_object_or_404(
        TrainingSession.objects.select_related('artwork', 'artwork__phase'),
        pk=pk,
    )
    return render(request, 'training/session_detail.html', {'session': session})


def session_log(request):
    sessions = TrainingSession.objects.select_related('artwork', 'artwork__phase')
    phase_filter = request.GET.get('phase')
    if phase_filter:
        sessions = sessions.filter(artwork__phase__number=phase_filter)
    phases = Phase.objects.all()
    return render(request, 'training/session_log.html', {
        'sessions': sessions[:50],
        'phases': phases,
        'phase_filter': phase_filter,
    })


def image_streaming(request):
    profile = UserProfile.get_instance()
    method = TrainingMethod.objects.filter(code='MET-1').first()
    return render(request, 'training/image_streaming.html', {
        'method': method,
        'is_flat_affect': profile.mode == 'flat_affect',
    })


def capture_list(request):
    captures = FieldCapture.objects.all()
    type_filter = request.GET.get('type')
    if type_filter:
        captures = captures.filter(capture_type=type_filter)
    return render(request, 'training/capture_list.html', {
        'captures': captures[:50],
        'type_filter': type_filter,
    })


def capture_new(request):
    if request.method == 'POST':
        form = FieldCaptureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training:capture_list')
    else:
        form = FieldCaptureForm()
    return render(request, 'training/capture_new.html', {'form': form})


def progress(request):
    total_sessions = TrainingSession.objects.count()
    total_captures = FieldCapture.objects.count()
    vviq_responses = VVIQResponse.objects.all()[:5]

    phase_stats = []
    for phase in Phase.objects.all():
        sessions = TrainingSession.objects.filter(artwork__phase=phase)
        avg = sessions.aggregate(
            avg_v=Avg('vividness_rating'),
            avg_s=Avg('stability_rating'),
            avg_d=Avg('detail_rating'),
            count=Count('id'),
        )
        phase_stats.append({
            'phase': phase,
            'count': avg['count'],
            'avg_vividness': avg['avg_v'],
            'avg_stability': avg['avg_s'],
            'avg_detail': avg['avg_d'],
        })

    return render(request, 'training/progress.html', {
        'total_sessions': total_sessions,
        'total_captures': total_captures,
        'vviq_responses': vviq_responses,
        'phase_stats': phase_stats,
    })


def vviq(request):
    if request.method == 'POST':
        form = VVIQForm(request.POST)
        if form.is_valid():
            item_scores = {}
            total = 0
            for i in range(1, 17):
                score = int(form.cleaned_data[f'item_{i}'])
                item_scores[str(i)] = score
                total += score

            VVIQResponse.objects.create(
                total_score=total,
                item_scores=item_scores,
                context=form.cleaned_data.get('context', ''),
            )

            profile = UserProfile.get_instance()
            if profile.vviq_baseline is None:
                profile.vviq_baseline = total
                profile.save()

            return redirect('training:progress')
    else:
        form = VVIQForm()
    return render(request, 'training/vviq.html', {'form': form})


def settings_view(request):
    profile = UserProfile.get_instance()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('training:settings')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'training/settings.html', {'form': form})


@require_POST
def api_update_timing(request, pk):
    session = get_object_or_404(TrainingSession, pk=pk)
    try:
        data = json.loads(request.body)
        if 'viewing_duration' in data:
            session.viewing_duration = int(data['viewing_duration'])
        if 'retention_duration' in data:
            session.retention_duration = int(data['retention_duration'])
        session.save()
        return JsonResponse({'status': 'ok'})
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'status': 'error'}, status=400)


def api_progress_data(request):
    sessions = TrainingSession.objects.filter(
        vividness_rating__isnull=False,
    ).order_by('date').values(
        'date', 'vividness_rating', 'stability_rating', 'detail_rating',
        'artwork__phase__number',
    )

    data = {
        'dates': [],
        'vividness': [],
        'stability': [],
        'detail': [],
        'phases': [],
    }
    for s in sessions:
        data['dates'].append(s['date'].strftime('%Y-%m-%d'))
        data['vividness'].append(s['vividness_rating'])
        data['stability'].append(s['stability_rating'])
        data['detail'].append(s['detail_rating'])
        data['phases'].append(s['artwork__phase__number'])

    vviq_data = list(VVIQResponse.objects.order_by('date').values('date', 'total_score'))
    data['vviq'] = {
        'dates': [v['date'].strftime('%Y-%m-%d') for v in vviq_data],
        'scores': [v['total_score'] for v in vviq_data],
    }

    return JsonResponse(data)
