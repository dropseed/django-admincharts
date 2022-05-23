window.addEventListener("DOMContentLoaded", function(event) {
    const configScript = document.getElementById("adminchart-chartjs-config");
    if (!configScript) return;
    const chartConfig = JSON.parse(configScript.textContent);
    if (!chartConfig) return;
    var container = document.getElementById('admincharts')
    var canvas = document.createElement("canvas")
    container.appendChild(canvas)
    var ctx = canvas.getContext('2d');
    var chart = new Chart(ctx, chartConfig);
});
