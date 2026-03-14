document.addEventListener('DOMContentLoaded', function() {
    const sessionId = document.getElementById('session-data')?.dataset.sessionId;
    const viewingDuration = parseInt(document.getElementById('session-data')?.dataset.viewingDuration || '60');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    const imagePhase = document.getElementById('image-phase');
    const retentionPhase = document.getElementById('retention-phase');
    const completePhase = document.getElementById('complete-phase');
    const countdownEl = document.getElementById('countdown');
    const countupEl = document.getElementById('countup');
    const startBtn = document.getElementById('start-btn');
    const endRetentionBtn = document.getElementById('end-retention-btn');

    let viewingTimer = null;
    let retentionTimer = null;
    let viewingSeconds = viewingDuration;
    let retentionSeconds = 0;
    let actualViewingDuration = 0;

    const bellSound = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdH2JkZeXk4yFfXd3fIWOlZqamJGJgXt4e4KLk5qcm5eSi4R+e3yBiZKYnJqWkImDfnt9g4uTmZyanJORioR+fH6Ei5OYmpuZk46IgX18f4aOlZmamZWPiIN+fH+Fj5WZmpqWkIqEf31/hY+WmZqalZCKhIB+f4WPlpmamZWQi4WAfn+Gj5aZmpmVkIuFgH+AhpCXmZqZlI+LhYCAgoiRl5mYl5KNiIKAgYWMk5iZmJSSjIeCgYOHjpSYmJeUkYyHg4KEiI+VmJeXk5CMh4OChYqRlpiXlpKOiYSChYmQlZeXlpKOiYWDhImQlZeWlpKPioWDhIqQlZeWlZKPioaDhYqRlZaWlZGOioaEhYuRlZaVlJGOioaFhouSlZaVlJGOi4eGh4ySlZWVk5COi4eGiI2TlZWUk4+Ni4iHiY2TlJSUk4+NjIiIio6TlJSTko+NjImJi4+TlJOSko+OjImKjJCTk5OSko+OjYqLjZGTk5KRkI+OjIuMjpGTk5GRkI+OjYyNj5GTkpGRkI+PjY2Oj5GTkpCQkI+PjY6PkJGSkJCQj4+Ojo+QkZGQkI+Pj4+PkJCRkZCPj4+Pj4+QkJCQkI+Pj4+Pj5CQkJCPj4+Pj4+PkJCQj4+Pj4+Pj5CQkI+Pj4+Pj4+QkJCPj4+Pj4+Pj5CQj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+P');

    function formatTime(seconds) {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    }

    function playBell() {
        try { bellSound.play(); } catch(e) {}
    }

    function startViewing() {
        startBtn.classList.add('hidden');
        imagePhase.classList.remove('hidden');

        viewingTimer = setInterval(function() {
            viewingSeconds--;
            actualViewingDuration++;
            countdownEl.textContent = formatTime(viewingSeconds);

            if (viewingSeconds <= 0) {
                clearInterval(viewingTimer);
                playBell();
                startRetention();
            }
        }, 1000);
    }

    function startRetention() {
        imagePhase.classList.add('hidden');
        retentionPhase.classList.remove('hidden');

        retentionTimer = setInterval(function() {
            retentionSeconds++;
            countupEl.textContent = formatTime(retentionSeconds);
        }, 1000);
    }

    function endRetention() {
        clearInterval(retentionTimer);
        retentionPhase.classList.add('hidden');
        completePhase.classList.remove('hidden');

        fetch(`/api/session/${sessionId}/update-timing/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                viewing_duration: actualViewingDuration,
                retention_duration: retentionSeconds,
            }),
        }).then(function() {
            setTimeout(function() {
                window.location.href = `/session/${sessionId}/assess/`;
            }, 1000);
        });
    }

    if (startBtn) startBtn.addEventListener('click', startViewing);
    if (endRetentionBtn) endRetentionBtn.addEventListener('click', endRetention);

    document.addEventListener('keydown', function(e) {
        if (e.code === 'Space' || e.code === 'Enter') {
            e.preventDefault();
            if (!startBtn.classList.contains('hidden')) {
                startViewing();
            } else if (!retentionPhase.classList.contains('hidden')) {
                endRetention();
            }
        }
        if (e.code === 'Escape') {
            if (viewingTimer) clearInterval(viewingTimer);
            if (retentionTimer) clearInterval(retentionTimer);
            window.location.href = '/sessions/';
        }
    });

    if (document.fullscreenEnabled) {
        document.addEventListener('click', function() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(function(){});
            }
        }, { once: true });
    }
});
