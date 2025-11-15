// German Learning Dashboard - JavaScript
// Loads and displays statistics from stats.json

let chart = null;

// Load stats when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
});

async function loadStats() {
    try {
        const response = await fetch('data/stats.json');
        if (!response.ok) {
            throw new Error('Failed to load stats');
        }

        const stats = await response.json();
        displayStats(stats);
    } catch (error) {
        console.error('Error loading stats:', error);
        showErrorState();
    }
}

function displayStats(stats) {
    // Update last updated time
    const lastUpdated = new Date(stats.last_updated);
    document.getElementById('lastUpdated').textContent = lastUpdated.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    // Overview Cards
    displayOverview(stats.overview);

    // Vocabulary Stats
    displayVocabulary(stats.vocabulary);

    // CEFR Progress
    displayCEFRProgress(stats.overview);

    // Daily Activity Chart
    displayActivityChart(stats.daily_activity);

    // Achievements
    displayAchievements(stats.achievements);

    // Milestones
    displayMilestones(stats.milestones);
}

function displayOverview(overview) {
    document.getElementById('currentLevel').textContent = `Level ${overview.current_level} (${overview.estimated_cefr})`;
    document.getElementById('totalXP').textContent = overview.total_xp.toLocaleString();
    document.getElementById('currentStreak').textContent = `${overview.current_streak} ${overview.current_streak === 1 ? 'day' : 'days'}`;
    document.getElementById('totalHours').textContent = `${overview.total_hours} hrs`;
}

function displayVocabulary(vocab) {
    document.getElementById('totalWords').textContent = vocab.total_words;
    document.getElementById('masteredWords').textContent = vocab.mastered;
    document.getElementById('vocabAccuracy').textContent = vocab.accuracy.toFixed(0);
}

function displayCEFRProgress(overview) {
    const currentLevel = overview.current_level;

    // CEFR level ranges
    const ranges = {
        'A1': { min: 1, max: 10 },
        'A2': { min: 11, max: 25 },
        'B1': { min: 26, max: 45 },
        'B2': { min: 46, max: 70 }
    };

    // Calculate progress for each CEFR level
    Object.keys(ranges).forEach(level => {
        const range = ranges[level];
        let progress = 0;

        if (currentLevel > range.max) {
            progress = 100;
        } else if (currentLevel >= range.min && currentLevel <= range.max) {
            progress = ((currentLevel - range.min + 1) / (range.max - range.min + 1)) * 100;
        }

        const fillElement = document.querySelector(`#cefr${level} .cefr-fill`);
        if (fillElement) {
            fillElement.style.width = `${progress}%`;
        }
    });
}

function displayActivityChart(dailyActivity) {
    const ctx = document.getElementById('activityChart');
    if (!ctx) return;

    // Prepare data
    const labels = dailyActivity.map(day => {
        const date = new Date(day.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });

    const minutes = dailyActivity.map(day => day.minutes);
    const xp = dailyActivity.map(day => day.xp);

    // Destroy existing chart if it exists
    if (chart) {
        chart.destroy();
    }

    // Create chart
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Minutes Studied',
                    data: minutes,
                    backgroundColor: 'rgba(74, 144, 226, 0.7)',
                    borderColor: 'rgba(74, 144, 226, 1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'XP Earned',
                    data: xp,
                    type: 'line',
                    backgroundColor: 'rgba(80, 200, 120, 0.2)',
                    borderColor: 'rgba(80, 200, 120, 1)',
                    borderWidth: 2,
                    fill: true,
                    yAxisID: 'y1',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#FAFAFA',
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(38, 39, 48, 0.9)',
                    titleColor: '#FAFAFA',
                    bodyColor: '#FAFAFA',
                    borderColor: '#4A90E2',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#B0B0B0',
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    ticks: {
                        color: '#B0B0B0'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    title: {
                        display: true,
                        text: 'Minutes',
                        color: '#4A90E2'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    ticks: {
                        color: '#B0B0B0'
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                    title: {
                        display: true,
                        text: 'XP',
                        color: '#50C878'
                    }
                }
            }
        }
    });

    // Set chart height
    ctx.style.height = '400px';
}

function displayAchievements(achievements) {
    const grid = document.getElementById('achievementsGrid');
    if (!grid) return;

    grid.innerHTML = '';

    if (achievements.length === 0) {
        grid.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🏆</div><p>No achievements unlocked yet. Keep learning!</p></div>';
        return;
    }

    achievements.forEach(achievement => {
        const card = document.createElement('div');
        card.className = 'achievement-card';

        const unlockedDate = achievement.unlocked_at ? new Date(achievement.unlocked_at).toLocaleDateString() : '';

        card.innerHTML = `
            <div class="achievement-icon">${achievement.icon}</div>
            <div class="achievement-title">${achievement.name}</div>
            <div class="achievement-desc">${achievement.description}</div>
            ${unlockedDate ? `<div class="achievement-date">Unlocked: ${unlockedDate}</div>` : ''}
        `;

        grid.appendChild(card);
    });
}

function displayMilestones(milestones) {
    const list = document.getElementById('milestonesList');
    if (!list) return;

    list.innerHTML = '';

    if (milestones.length === 0) {
        list.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🎯</div><p>Milestones will appear as you progress!</p></div>';
        return;
    }

    milestones.forEach(milestone => {
        const item = document.createElement('div');
        item.className = 'milestone-item';
        item.innerHTML = `
            <div class="milestone-icon">${milestone.icon}</div>
            <div class="milestone-text">${milestone.milestone}</div>
        `;
        list.appendChild(item);
    });
}

function showErrorState() {
    document.getElementById('lastUpdated').textContent = 'Error loading data';
    document.getElementById('currentLevel').textContent = '-';
    document.getElementById('totalXP').textContent = '-';
    document.getElementById('currentStreak').textContent = '-';
    document.getElementById('totalHours').textContent = '-';

    // Show error message
    const container = document.querySelector('.container');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'empty-state';
    errorDiv.innerHTML = `
        <div class="empty-state-icon">⚠️</div>
        <p>Failed to load statistics. Please try again later.</p>
        <p style="font-size: 0.8em; margin-top: 8px;">Make sure stats.json exists in the data/ folder.</p>
    `;
    container.insertBefore(errorDiv, container.querySelector('.overview-cards'));
}
