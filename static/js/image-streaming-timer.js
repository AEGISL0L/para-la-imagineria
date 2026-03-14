document.addEventListener('DOMContentLoaded', function() {
    const timerDisplay = document.getElementById('is-timer');
    const startBtn = document.getElementById('is-start');
    const pauseBtn = document.getElementById('is-pause');
    const resetBtn = document.getElementById('is-reset');
    const durationSelect = document.getElementById('is-duration');
    const progressBar = document.getElementById('is-progress');
    const statusText = document.getElementById('is-status');
    const promptEl = document.getElementById('is-prompt');

    const prompts = [
        'Describe en voz alta todo lo que ves en tu mente...',
        'Enfócate en los colores que aparecen...',
        'Nota las formas y sus bordes...',
        'Observa el movimiento si lo hay...',
        'Describe la textura de lo que ves...',
        'Nota la iluminación de la escena...',
        'Describe la profundidad del espacio...',
        'Observa los detalles más pequeños...',
    ];

    let timer = null;
    let elapsed = 0;
    let duration = 600;
    let promptIndex = 0;

    function formatTime(seconds) {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    }

    function updateDisplay() {
        const remaining = duration - elapsed;
        timerDisplay.textContent = formatTime(remaining);
        const pct = (elapsed / duration) * 100;
        progressBar.style.width = pct + '%';
    }

    function rotatePrompt() {
        if (promptEl) {
            promptEl.textContent = prompts[promptIndex % prompts.length];
            promptIndex++;
        }
    }

    function start() {
        duration = parseInt(durationSelect.value);
        startBtn.classList.add('hidden');
        pauseBtn.classList.remove('hidden');
        statusText.textContent = 'En curso...';
        rotatePrompt();

        timer = setInterval(function() {
            elapsed++;
            updateDisplay();

            if (elapsed % 120 === 0) rotatePrompt();

            if (elapsed >= duration) {
                clearInterval(timer);
                statusText.textContent = 'Completado';
                pauseBtn.classList.add('hidden');
                resetBtn.classList.remove('hidden');
                try {
                    new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQ==').play();
                } catch(e) {}
            }
        }, 1000);
    }

    function pause() {
        clearInterval(timer);
        timer = null;
        pauseBtn.classList.add('hidden');
        startBtn.classList.remove('hidden');
        startBtn.textContent = 'Continuar';
        statusText.textContent = 'Pausado';
    }

    function reset() {
        clearInterval(timer);
        timer = null;
        elapsed = 0;
        promptIndex = 0;
        updateDisplay();
        resetBtn.classList.add('hidden');
        startBtn.classList.remove('hidden');
        startBtn.textContent = 'Iniciar';
        statusText.textContent = 'Listo';
        if (promptEl) promptEl.textContent = '';
    }

    if (startBtn) startBtn.addEventListener('click', start);
    if (pauseBtn) pauseBtn.addEventListener('click', pause);
    if (resetBtn) resetBtn.addEventListener('click', reset);
    if (durationSelect) {
        durationSelect.addEventListener('change', function() {
            if (!timer) {
                duration = parseInt(this.value);
                elapsed = 0;
                updateDisplay();
            }
        });
    }

    updateDisplay();
});
