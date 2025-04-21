// File: dashboard/static/js/scripts.js

/**
 * Updates the dashboard with the latest migration progress and status data.
 * This function will be called periodically to keep the dashboard data up-to-date.
 */
function updateDashboard() {
    fetch('/migration/progress')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateMigrationProgress(data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });

    fetch('/migration/status')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateMigrationStatus(data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

/**
 * Updates the migration progress section of the dashboard with new data.
 * @param {Object} data - The migration progress data.
 */
function updateMigrationProgress(data) {
    const progressElement = document.getElementById('migration-progress');
    if (progressElement) {
        progressElement.textContent = data.progress;
    }
}

/**
 * Updates the migration status section of the dashboard with new data.
 * @param {Object} data - The migration status data.
 */
function updateMigrationStatus(data) {
    const statusElement = document.getElementById('migration-status');
    if (statusElement) {
        statusElement.textContent = data.status;
    }
}

// Set an interval to periodically update the dashboard
const updateInterval = 30000; // 30 seconds
setInterval(updateDashboard, updateInterval);

// Initialize the dashboard data on page load
document.addEventListener('DOMContentLoaded', (event) => {
    updateDashboard();
});
