/**
 * Chart.js — premium dark theme styling.
 */

const CHART_THEME = {
    text: '#94A3B8',
    grid: '#25344F',
    palette: [
        '#3B82F6', '#22C55E', '#EAB308', '#EF4444',
        '#8B5CF6', '#EC4899', '#14B8A6', '#F97316',
    ],
};

function hideChartSkeleton(wrapperId) {
    const wrapper = document.getElementById(wrapperId);
    if (!wrapper) return;
    const skeleton = wrapper.querySelector('.chart-skeleton');
    if (skeleton) {
        skeleton.classList.add('hidden');
        setTimeout(() => skeleton.remove(), 260);
    }
}

function initDashboardCharts(barLabels, barValues, pieLabels, pieValues, spendingLabel) {
    if (typeof Chart === 'undefined') return;

    const label = spendingLabel || 'Spending';

    Chart.defaults.color = CHART_THEME.text;
    Chart.defaults.borderColor = CHART_THEME.grid;
    Chart.defaults.font.family = "'Inter', sans-serif";

    const sharedOptions = {
        responsive: true,
        maintainAspectRatio: true,
        animation: { duration: 400, easing: 'easeOutQuart' },
    };

    const barEl = document.getElementById('barChart');
    if (barEl && barValues.some((v) => v > 0)) {
        new Chart(barEl, {
            type: 'bar',
            data: {
                labels: barLabels,
                datasets: [{
                    label: label,
                    data: barValues,
                    backgroundColor: CHART_THEME.palette[0],
                    hoverBackgroundColor: '#4F8DF7',
                    borderRadius: 6,
                    borderSkipped: false,
                }],
            },
            options: {
                ...sharedOptions,
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        grid: { display: false },
                        border: { color: CHART_THEME.grid },
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: CHART_THEME.grid },
                        border: { display: false },
                        ticks: {
                            callback: (v) => '$' + v,
                            padding: 8,
                        },
                    },
                },
            },
        });
        hideChartSkeleton('barChartWrapper');
    }

    const pieEl = document.getElementById('pieChart');
    if (pieEl && pieValues.some((v) => v > 0)) {
        new Chart(pieEl, {
            type: 'doughnut',
            data: {
                labels: pieLabels,
                datasets: [{
                    data: pieValues,
                    backgroundColor: CHART_THEME.palette.slice(0, pieLabels.length),
                    borderColor: '#162033',
                    borderWidth: 2,
                    hoverOffset: 6,
                }],
            },
            options: {
                ...sharedOptions,
                cutout: '62%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { padding: 16, usePointStyle: true, pointStyle: 'circle' },
                    },
                },
            },
        });
        hideChartSkeleton('pieChartWrapper');
    }
}
