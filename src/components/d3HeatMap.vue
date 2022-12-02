<template>
    <div >
        <div class="text-right mt-n12">
            <v-btn icon @click="downloadPng()"><v-icon>mdi-monitor-arrow-down-variant</v-icon></v-btn>
        </div>
        <div id="my_dataviz" class="svg-container"></div>
    </div>
    
</template>
<script>
//references
/*
Initial Code
https://d3-graph-gallery.com/graph/heatmap_style.html

Legend
https://www.visualcinnamon.com/2016/05/smooth-color-legend-d3-svg-gradient/

Resize d3
https://chartio.com/resources/tutorials/how-to-resize-an-svg-when-the-window-is-resized-in-d3-js/

*/

//General Functions
import * as d3 from 'd3'
import d3ToPng from 'd3-svg-to-png'

const rangeToPercent = (val)  => { return ( (val + 1) / 2) * 100 + '%' }

const colorsArray = (threshold) => {
    return [
        {value: -1, color: "#4A148C"},
//        {value: -threshold, color: "#4A148C"},
        {value: -threshold +.1, color: "#AB47BC"},
        {value: 0, color: "white"},
        {value: threshold -.1, color: "#42A5F5"},
//        {value: threshold, color: "#0D47A1"},
        {value: 1, color: "#0D47A1"}
    ]
}


const buildGradientData = (threshold) => {
   let gradientData = []
   colorsArray(threshold).forEach(item => {
        gradientData.push(
            {offset: rangeToPercent(item.value), color: item.color}
        )
   })
   return gradientData
}
const buildColorScale = (threshold) => {
    let domain = []
    let range = []
    colorsArray(threshold).forEach(item => {
        domain.push(item.value)
        range.push(item.color)
    })
    return d3.scaleLinear()
        .domain(domain)
        .range(range)
}

export default {
    name: 'd3HeatMap',
    props: [
        'heatMapXYVal',
        'threshold',
    ],
    data() {
        return {

        }
    },
    watch: {
        heatMapXYVal:  function(n,o) {
            n
            o
            if (this.heatMapXYVal != null) {
                this.drawHeatMap(this.formatAPIdata(this.heatMapXYVal), this.threshold)
                
            }
        }
    },
    mounted() {

        if (this.heatMapXYVal != null) {
                this.drawHeatMap(this.formatAPIdata(this.heatMapXYVal), this.threshold)
                
            
        }
    },
    methods: {
        
        formatAPIdata(rawData){
            let data = []
            rawData.forEach(item => {
                let obj = {}
                obj['group'] = item.x
                obj['variable'] = item.y
                obj['value'] = item.val
                data.push(obj)
            })
            return data
        },
        recolorLegend(threshold) {
            const linearGradient = d3.select("#linear-gradient")
            console.log(buildGradientData(threshold))
            linearGradient.selectAll("stop").data(buildGradientData(threshold))
            console.log('linearGradient',linearGradient)

            linearGradient.selectAll("stop")
                .transition().duration(1000)
                .attr("offset", function(d) { return d.offset; })
                .attr("stop-color", function(d) { return d.color; });

            const scale = d3.select('#legend rect')
            scale.style("fill", "url(#linear-gradient)");

        },
        recolorHeatMap(threshold) {
            this.recolorLegend(threshold)
            const colorScale = buildColorScale(threshold)                        
            const graph = d3.select("#graph")
            graph.selectAll('rect')
                .transition().duration(500)
                .style("fill", function(d) { return colorScale(d.value)} )
        },
        drawHeatMap(data, threshold) {
            /* eslint-disable */
            // set the dimensions and margins of the graph
            const margin = {top: 100, right: 100, bottom: 300, left: 300},
                width = 900 - margin.left - margin.right,
                height = 900 - margin.top - margin.bottom;
                
                // append the svg object to the body of the page
                const svg = d3.select("#my_dataviz")
                .append("svg")
                .attr("preserveAspectRatio", "xMinYMin meet")
                .attr("viewBox", "0 0 900 900")
                .style("background-color", "white")
                .classed("svg-content", true)   


                .append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);
                

                //DRAW KEY
                var defs = svg.append("defs");      
                var linearGradient = defs.append("linearGradient")
                    .attr("id", "linear-gradient");   
                    
                //convert correlation scale to color scale percentage 


                linearGradient.selectAll("stop")
                .data(buildGradientData(threshold))
                .enter().append("stop")
                .attr("offset", function(d) { return d.offset; })
                .attr("stop-color", function(d) { return d.color; });         
                const legend = svg.append("g").attr('id', 'legend')
                legend.append("rect")
                    .attr("x", 55).attr("y", -60)
                    .attr("width", 400)
                    .attr("height", 20)
                    .attr("rx", 10)
                    .attr("ry", 10)
                    .style("stroke", "grey")                    
                    .style("fill", "url(#linear-gradient)");
                legend.append("text").text(-1).attr("x", 55).attr("y", -25)
                legend.append("text").text(0).attr("x", 250).attr("y", -25)
                legend.append("text").text(1).attr("x", 440).attr("y", -25)


                
                // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
                var myGroups = Array.from(new Set(data.map(d => d.group)))
                var myVars = Array.from(new Set(data.map(d => d.variable)))

                // Build X scales and axis:


                const x = d3.scaleBand()
                    .range([ 0, width ])
                    .domain(myGroups)
                    .padding(0.05);
                svg.append("g")
                    .style("font-size", 15)
                    .attr("transform", `translate(10, ${height})`)

                    .call(d3.axisBottom(x).tickSize(0))
                    .selectAll("text")
                    .style("text-anchor", "start")
                    .attr("transform", "rotate(65)")
                
                // Build Y scales and axis:
                const y = d3.scaleBand()
                    .range([ height, 0 ])
                    .domain(myVars)
                    .padding(0.05);
                svg.append("g")
                    .style("font-size", 15)
                    .call(d3.axisLeft(y).tickSize(0))
                    .select(".domain").remove()
                    
                
                // Build color scale=
                const colorScale = buildColorScale(threshold)



                // create a tooltip
                const tooltip = d3.select("#my_dataviz")
                    .append("div")
                    .style("opacity", 0)
                    .style("position", "absolute")
                    .attr("class", "tooltip")
                    .style("background-color", "white")
                    .style("border", "solid 1px grey")
                    .style("border-radius", "10px")
                    .style("padding", "5px")
                    .classed("pa-3", true)
                
                // Three function that change the tooltip when user hover / move / leave a cell
                const mouseover = function(event,d) {
                    tooltip
                    .style("opacity", 1)
                    d3.select(this)
                    .style("stroke", 'black')
                    .style("opacity", 1)
                }
                const mousemove = function(event,d) {
                    tooltip
                    .html(`<div>x: ${d.group}</div><div>y: ${d.variable}</div><div>correlation: ${d.value}</div>`)
                    .style("left", (event.layerX) + "px")
                    .style("top", (event.layerY) + "px")

                }
                const mouseleave = function(event,d) {
                    tooltip
                    .style("opacity", 0)
                    d3.select(this)
                    .style("stroke", "none")
                    .style("opacity", 1.0)
                }


                // add the squares
                const graph = svg.append("g").attr('id', 'graph')
                graph.selectAll()
                    .data(data, function(d) {return d.group+':'+d.variable;})
                    .join("rect")
                    
                    .attr("x", function(d) { return x(d.group) })
                    .attr("y", function(d) { return y(d.variable) })
                    .attr("rx", 0)
                    .attr("ry", 0)
                    .attr("width", x.bandwidth() )
                    .attr("height", y.bandwidth() )
                    .style("fill", function(d) { return colorScale(d.value)} )
                    .style("stroke-width", 2)
                    .style("stroke", "white")
                    .style("opacity", 0.9)
                    .on("mouseover", mouseover)
                    .on("mousemove", mousemove)
                    .on("mouseleave", mouseleave)
        },
        downloadPng() {
            const svg = document.querySelector('svg')
            //library to export svg to png
            d3ToPng('svg', 'heatmap', {download: true})
        }
    }
}


</script>
<style scoped>
    .svg-container {
        display: inline-block;
        position: relative;
        width: 100%;
        max-width: 1000px;
        vertical-align: top;
        overflow: hidden;
    }
    .svg-content {
        display: inline-block;
        position: absolute;
        top: 0;
        left: 0;
    }    
</style>