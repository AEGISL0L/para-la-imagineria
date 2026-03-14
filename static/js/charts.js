document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/progress-data/')
        .then(r => r.json())
        .then(data => {
            if (data.dates.length === 0) {
                document.getElementById('charts-container').innerHTML =
                    '<p class="text-gray-500 dark:text-gray-400 text-center py-8">No hay sesiones con evaluaciones todavía.</p>';
                return;
            }

            const ratingsCtx = document.getElementById('ratings-chart');
            if (ratingsCtx) {
                new Chart(ratingsCtx, {
                    type: 'line',
                    data: {
                        labels: data.dates,
                        datasets: [
                            {
                                label: 'Viveza',
                                data: data.vividness,
                                borderColor: 'rgb(99, 102, 241)',
                                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                                tension: 0.3,
                                fill: true,
                            },
                            {
                                label: 'Estabilidad',
                                data: data.stability,
                                borderColor: 'rgb(16, 185, 129)',
                                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                                tension: 0.3,
                                fill: true,
                            },
                            {
                                label: 'Detalle',
                                data: data.detail,
                                borderColor: 'rgb(245, 158, 11)',
                                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                                tension: 0.3,
                                fill: true,
                            },
                        ],
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { min: 1, max: 10, title: { display: true, text: 'Puntuación' } },
                            x: { title: { display: true, text: 'Fecha' } },
                        },
                        plugins: {
                            legend: { position: 'top' },
                            title: { display: true, text: 'Evolución de puntuaciones' },
                        },
                    },
                });
            }

            const phaseCtx = document.getElementById('phase-chart');
            if (phaseCtx) {
                const phaseCounts = [0, 0, 0, 0, 0, 0];
                data.phases.forEach(p => { if (p >= 1 && p <= 6) phaseCounts[p - 1]++; });

                new Chart(phaseCtx, {
                    type: 'bar',
                    data: {
                        labels: ['Fase 1', 'Fase 2', 'Fase 3', 'Fase 4', 'Fase 5', 'Fase 6'],
                        datasets: [{
                            label: 'Sesiones',
                            data: phaseCounts,
                            backgroundColor: [
                                'rgba(107, 114, 128, 0.7)',
                                'rgba(59, 130, 246, 0.7)',
                                'rgba(245, 158, 11, 0.7)',
                                'rgba(99, 102, 241, 0.7)',
                                'rgba(16, 185, 129, 0.7)',
                                'rgba(168, 85, 247, 0.7)',
                            ],
                        }],
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: { display: true, text: 'Sesiones por fase' },
                            legend: { display: false },
                        },
                    },
                });
            }

            const vviqCtx = document.getElementById('vviq-chart');
            if (vviqCtx && data.vviq && data.vviq.dates.length > 0) {
                new Chart(vviqCtx, {
                    type: 'line',
                    data: {
                        labels: data.vviq.dates,
                        datasets: [{
                            label: 'VVIQ Total',
                            data: data.vviq.scores,
                            borderColor: 'rgb(168, 85, 247)',
                            backgroundColor: 'rgba(168, 85, 247, 0.1)',
                            tension: 0.3,
                            fill: true,
                        }],
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { min: 16, max: 80, title: { display: true, text: 'Puntuación VVIQ' } },
                        },
                        plugins: {
                            title: { display: true, text: 'Evolución VVIQ' },
                        },
                    },
                });
            }
        });
});
