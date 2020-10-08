<template>
<div :id="targetId"></div>
</template>

<script>
import * as d3 from 'd3'
import d3Tip from 'd3-tip'

export default {
  mounted() {
    this.barChart(this.targetId)
  },
  computed: {
    targetId() {
      return this.$props.target
    },
    voteData() {
      return this.$props.values
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

      const height = Math.ceil((this.voteData.length + 0.1) * barHeight) + margin.top + margin.bottom

      const width = 1000

      const x = d3.scaleLinear()
        .domain([0, 100])
        .range([margin.left, width - margin.right])

      const y = d3.scaleBand()
        .domain(d3.range(this.voteData.length))
        .rangeRound([margin.top, height - margin.bottom])
        .padding(0.1)

      const tooltip = d3Tip().html((EVENT, d) => {
        return `<div class="tooltip bg-color-nav text-color-nav rounded text-xs px-3 py-2">${d.label}, ${d.percentage}%</div>`
      })

      const svg = d3.select(`#${targetId}`).append('svg')
        .attr('viewBox', `0 0 ${width} ${height}`)
        .attr('preserveAspectRatio', 'xMinYMin meet')

      svg.append('g')
        .attr('fill', 'currentColor')
        .attr('class', 'text-color-image')
        .selectAll('rect')
        .data(this.voteData)
        .join('rect')
        .attr('x', x(0))
        .attr('y', (d, i) => y(i))
        .attr('width', d => x(100))
        .attr('height', y.bandwidth())
        .on('mousemove', function(event, d) {
          tooltip.show(event, d, this)
          const tooltipWidth = document.querySelector('.tooltip').clientWidth
          tooltip.style('top', `${(event.pageY - 45)}px`)
          tooltip.style('left', `${(event.pageX - (tooltipWidth / 2))}px`)
        })
        .on('mouseleave', function(event, d) {
          tooltip.hide(event, d, this)
        })

      svg.append('g')
        .attr('fill', 'currentColor')
        .attr('class', 'text-color-sale')
        .selectAll('rect')
        .data(this.voteData)
        .join('rect')
        .attr('x', x(0))
        .attr('y', (d, i) => y(i))
        .attr('width', d => x(d.percentage) - x(0))
        .attr('height', y.bandwidth())
        .on('mousemove', function(event, d) {
          tooltip.show(event, d, this)
          const tooltipWidth = document.querySelector('.tooltip').clientWidth
          tooltip.style('top', `${(event.pageY - 45)}px`)
          tooltip.style('left', `${(event.pageX - (tooltipWidth / 2))}px`)
        })
        .on('mouseleave', function(event, d) {
          tooltip.hide(event, d, this)
        })

      svg.append('g')
        .attr('fill', 'currentColor')
        .attr('class', 'text-color-nav')
        .attr('text-anchor', 'end')
        .attr('font-family', 'sans')
        .attr('font-size', 12)
        .selectAll('text')
        .data(this.voteData)
        .join('text')
        .attr('x', d => x(100))
        .attr('y', (d, i) => y(i) + y.bandwidth() / 2)
        .attr('dy', '0.35em')
        .attr('dx', -5)
        .text(d => `${d.percentage}%`)

      svg.append('g')
        .attr('fill', 'currentColor')
        .attr('class', 'text-color-nav')
        .attr('text-anchor', 'start')
        .attr('font-family', 'sans')
        .attr('font-size', 12)
        .selectAll('text')
        .data(this.voteData)
        .join('text')
        .attr('x', '0.35em')
        .attr('y', (d, i) => y(i) + y.bandwidth() / 2)
        .attr('dy', '0.35em')
        .attr('dx', 0)
        .text(d => `${d.label}`)

      svg.call(tooltip)
    }
  }
}
</script>
