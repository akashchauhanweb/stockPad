// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["HEROMOTOCO", "HINDUNILVR", "IRCTC", "MARUTI", "RBLBANK", "SPICEJET", "SUNPHARMA"],
    datasets: [{
      data: jshares,
      backgroundColor: ['#4e73df', '#00d9e0', '#36b9cc', '#2c2caf', '#781cc8', '#af2cad', '#cc33a1'],
      hoverBackgroundColor: ['#2e59d9', '#00b4ba', '#2c9faf','#22228a','#5a1299','#852183','#ab2986'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
