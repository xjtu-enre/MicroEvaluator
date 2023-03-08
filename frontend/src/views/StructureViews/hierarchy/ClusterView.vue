<template>
  <div id="chart"></div>
</template>

<script>
import {getClusterDatas} from "../../../api/project";
import * as d3 from 'd3';

export default {
  name: "ClusterView",
  created() {
    this.drawSvg()
  },
  methods: {
    drawSvg() {
      getClusterDatas()
        .then(res => {
          const width = 932, height = 932;
          const root = d3.pack()
            .size([width * 0.6, height * 0.6])
            .radius(d => d.data.value)
            .padding(0.05)(d3.hierarchy({name: "root", children: JSON.parse(res.data).cluster})
              .sum(d => d.value)
              .sort((a, b) => b.value - a.value));
          let focus = root;
          let view;

          const color = d3.scaleSequential(d3.interpolateSinebow).domain([0, 8])

          const distinctValues = [0,1,2,3,4,5]

          const posY = d3.scaleLinear().range([-400,-380])


          const svg = d3.select("#chart").append("svg")
            .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
            .style("display", "block")
            .style("margin", "0 -14px")
            .style("background", "hsl(170,80%,80%)")
            .style("cursor", "pointer")
            .on("click", (event) => zoom(event, root))

          svg
            .append('g')
            .selectAll('circle')
            .data(distinctValues)
            .join('circle')
            .attr('cx', -400)
            .attr('cy', d => posY(d))
            .attr('opacity', 1)
            .attr('fill', d => color(d))
            .attr('r', 5);

          svg
            .append('g')
            .selectAll('text')
            .data(distinctValues)
            .join('text')
            .text(d => d)
            .attr('font-size', 14)
            .style('text-anchor', 'left')
            .attr('dx', -400 + 10)
            .attr('dy', d => posY(d) + 5);



          const node = svg.append("g")
            .selectAll("circle")
            .data(root.descendants().slice(1))
            .join("circle")
            // .attr("fill", d => d.children ? color(d.depth) : "white")
            .attr("fill", d => d.children ? "hsl(100,80%,80%)" : color(d.data.color))
            .attr("pointer-events", d => !d.children ? "none" : null)
            .on("mouseover", function () {
              d3.select(this).attr("stroke", "#000");
            })
            .on("mouseout", function () {
              d3.select(this).attr("stroke", null);
            })
            .on("click", (event, d) => focus !== d && (zoom(event, d), event.stopPropagation()));

          const label = svg.append("g")
            .style("font", "10px sans-serif")
            .attr("pointer-events", "none")
            .attr("text-anchor", "middle")
            .selectAll("text")
            .data(root.descendants())
            .join("text")
            .style("fill-opacity", d => d.parent === root ? 1 : 0)
            .style("display", d => d.parent === root ? "inline" : "none")
            .text(function (d) {
              return d.depth===1?d.data.name:'';
            });

          zoomTo([root.x, root.y, root.r * 2]);

          function zoomTo(v) {
            const k = width / v[2] / 1.5;

            view = v;
            console.log(v)
            label.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
            node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
            node.attr("r", d => d.r * k);
          }

          function zoom(event, d) {

            focus = d;

            const transition = svg.transition()
              .duration(event.altKey ? 7500 : 750)
              // eslint-disable-next-line no-unused-vars
              .tween("zoom", d => {
                const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2]);
                return t => zoomTo(i(t));
              });

            label
              .filter(function (d) {
                return d.parent === focus || this.style.display === "inline";
              })
              .transition(transition)
              .style("fill-opacity", d => d.parent === focus ? 1 : 0)
              .on("start", function (d) {
                if (d.parent === focus) this.style.display = "inline";
              })
              .on("end", function (d) {
                if (d.parent !== focus) this.style.display = "none";
              });
          }
        })
    }
  }
}
</script>

<style scoped>

</style>
