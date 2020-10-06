<template>
<div>
  <bar-chart :data="chartData" :options="chartOptions" :height="chartHeight" />
</div>
</template>

<script>
Chart.Tooltip.positioners.cursor = function(chartElements, coordinates) {
  return coordinates;
}

export default {
  mounted() {
    console.log(this.chartLabels)
    console.log(this.datsetData)
  },
  props: ['dataForms'],
  computed: {
    chartLabels() {
      return this.$props.dataForms.filter(e => e).map(({
        value
      }) => value)
    },
    datsetData() {
      return this.$props.dataForms.filter(e => e).map((v) => Math.floor(Math.random() * 150 + 1))
    },
    chartHeight() {
      return this.chartLabels.length * 15
    },
    chartData() {
      return {
        labels: this.chartLabels,
        datasets: [{
          label: 'Ja',
          backgroundColor: '#1371d1',
          data: this.datsetData
        }]
      }
    }
  },
  data() {
    return {
      chartOptions: {
        responsive: true,
        layout: {
          padding: {
            top: -20,
            right: -20,
            bottom: -20,
            left: -20
          }
        },
        hover: {
          intersect: true
        },
        legend: {
          display: false
        },
        title: {
          display: false
        },
        tooltips: {
          backgroundColor: '#17BF62',
          enabled: true,
          intersect: true,
          position: 'cursor',
          mode: 'label'
        },
        animation: {
          animateScale: true
        },
        scales: {
          xAxes: [{
            ticks: {
              display: false,
              beginAtZero: true
            },
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            ticks: {
              display: false,
              beginAtZero: true
            },
            gridLines: {
              display: false
            }
          }]
        }
      }
    }
  }
}
</script>
