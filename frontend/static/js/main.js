document.addEventListener("DOMContentLoaded", function () {
    const dataContainer = document.getElementById("chartDataContainer");
    if (!dataContainer) return;

    // Parse JSON data safely from data attributes
    const expiryChartData = JSON.parse(dataContainer.dataset.expiry || "[]");
    const stockLabels = JSON.parse(dataContainer.dataset.labels || "[]");
    const stockData = JSON.parse(dataContainer.dataset.stock || "[]");

    // Expiry Breakdown Donut Chart
    const expiryCanvas = document.getElementById('expiryChart');
    if (expiryCanvas) {
        new Chart(expiryCanvas.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Valid Stock', 'Expiring Soon (<30 Days)', 'Expired'],
                datasets: [{
                    data: expiryChartData,
                    backgroundColor: ['#198754', '#ffc107', '#dc3545']
                }]
            },
            options: { 
                responsive: true, 
                maintainAspectRatio: false 
            }
        });
    }

    // Storage Level Bar Chart
    const stockCanvas = document.getElementById('stockChart');
    if (stockCanvas) {
        new Chart(stockCanvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels: stockLabels,
                datasets: [{
                    label: 'Remaining Valid Units',
                    data: stockData,
                    backgroundColor: '#0d6efd'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { 
                    y: { 
                        beginAtZero: true 
                    } 
                }
            }
        });
    }
});