// Read chart data from the JSON script tag
const dataEl = document.getElementById("chart-data");
const chartData = dataEl
  ? JSON.parse(dataEl.textContent)
  : { expiry: [], labels: [], stock: [] };

// --- Expiry Doughnut Chart ---
const expiryCanvas = document.getElementById("expiryChart");
if (expiryCanvas) {
  new Chart(expiryCanvas, {
    type: "doughnut",
    data: {
      labels: ["Valid", "Expiring Soon", "Expired"],
      datasets: [
        {
          data: chartData.expiry,
          backgroundColor: ["#198754", "#ffc107", "#dc3545"],
          borderWidth: 2,
          borderColor: "#fff",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "bottom" } },
    },
  });
}

// --- Stock Bar Chart ---
const stockCanvas = document.getElementById("stockChart");
if (stockCanvas) {
  new Chart(stockCanvas, {
    type: "bar",
    data: {
      labels: chartData.labels,
      datasets: [
        {
          label: "Quantity in Stock",
          data: chartData.stock,
          backgroundColor: "#0d6efd",
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, title: { display: true, text: "Units" } },
        x: {
          ticks: {
            autoSkip: false,
            maxRotation: 45,
            minRotation: 45,
            font: { size: 10 },
          },
        },
      },
    },
  });
}
