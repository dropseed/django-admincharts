window.addEventListener("DOMContentLoaded", function(event) {
    const chartConfig = JSON.parse(document.getElementById("adminchart-chartjs-config").textContent);
    if (!chartConfig) return;
    var container = document.getElementById('admincharts')
    var canvas = document.createElement("canvas")
    container.appendChild(canvas)
    var ctx = canvas.getContext('2d');
    var chart = new Chart(ctx, chartConfig);
});
