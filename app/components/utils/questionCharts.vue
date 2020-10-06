<template>
<div :id="targetId"></div>
</template>

<script>
import * as d3 from 'd3'
import d3Tip from 'd3-tip'

export default {
  mounted() {
    const forms = this.chartLabels
    this.barChart(this.targetId)
  },
  computed: {
    chartLabels() {
      return this.$props.values.filter(e => e).map(({
        value
      }) => value)
    },
    mockData() {
      return this.chartLabels.filter((e) => e).map((v) => {
        return {
          'votes': Math.floor(Math.random() * 100 + 1),
          'value': v
        }
      })
    },
    formData() {
      return this.$props.values
    },
    targetId() {
      return this.$props.target
    }
  },
  props: ['values', 'target'],
  methods: {
    barChart(targetId) {
      const barHeight = 30

      const margin = ({
        top: 10,
        right: 0,
        bottom: 0,
        left: 0
      })

      const height = Math.ceil((this.mockData.length + 0.1) * barHeight) + margin.top + margin.bottom

      const width = 1000

      const x = d3.scaleLinear()
        .domain([0, 100])
        .range([margin.left, width - margin.right])

      const y = d3.scaleBand()
        .domain(d3.range(this.mockData.length))
        .rangeRound([margin.top, height - margin.bottom])
        .padding(0.1)

      const tooltip = d3Tip().html((EVENT, d) => {
        return `<div class="bg-color-nav text-color-nav rounded text-xs px-3 py-2">${d.value}, ${d.votes}%</div>`
      })

      const svg = d3.select(`#${targetId}`).append('svg')
        .attr('viewBox', `0 0 ${width} ${height}`)
        .attr('preserveAspectRatio', 'xMinYMin meet')

      svg.append('g')
        .attr('fill', 'currentColor')
        .attr('class', 'text-color-sale')
        .selectAll('rect')
        .data(this.mockData)
        .join('rect')
        .attr('x', x(0))
        .attr('y', (d, i) => y(i))
        .on('mousemove', function(event, d) {
          tooltip.show(event, d, this)
          tooltip.style('top', `${(event.y + 10)}px`)
          tooltip.style('left', `${(event.x + 10)}px`)
        })
        .on('mouseleave', function(event, d) {
          tooltip.hide(event, d, this)
        })
        .attr('width', d => x(d.votes) - x(0))
        .attr('height', y.bandwidth())

      svg.append('g')
        .attr('fill', 'currentColor')
        .attr('class', 'text-color-nav')
        .attr('text-anchor', 'end')
        .attr('font-family', 'sans')
        .attr('font-size', 12)
        .selectAll('text')
        .data(this.mockData)
        .join('text')
        .attr('x', d => x(d.votes))
        .attr('y', (d, i) => y(i) + y.bandwidth() / 2)
        .attr('dy', '0.35em')
        .attr('dx', -4)
        .text(d => `${d.votes}%`)
        .call(text => text.filter(d => x(d.votes) - x(0) < 30)
          .attr('dx', +4)
          .attr('fill', 'black')
          .attr('text-anchor', 'start'))


      svg.call(tooltip)
    }
  }
}
</script>
