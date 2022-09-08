<template>
    <div >
        <div id="my_dataviz"></div>
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


import * as d3 from 'd3'
export default {
    name: 'd3Test',

    data() {
        return {

        }
    },
    watch: {

    },
    mounted() {
        d3.json('https://clynx.s3.amazonaws.com/milo/test_data.json').then(rawData => {
                    console.log(rawData)
                    let data = []
                    rawData.forEach(item => {
                        let obj = {}
                        obj['group'] = item.x
                        obj['variable'] = item.y
                        obj['value'] = item.val
                        data.push(obj)
                    })
                    this.drawHeatMap(data)
                })        


    },
    methods: {
        


        drawHeatMap(data) {
            data
            /* eslint-disable */
            // set the dimensions and margins of the graph
            const margin = {top: 100, right: 50, bottom: 200, left: 200},
                width = 900 - margin.left - margin.right,
                height = 900 - margin.top - margin.bottom;
                
                // append the svg object to the body of the page
                const svg = d3.select("#my_dataviz")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);
                
                //DRAW KEY
                var defs = svg.append("defs");      
                var linearGradient = defs.append("linearGradient")
                    .attr("id", "linear-gradient");   
                    
                //convert correlation scale to color scale percentage 
                 const rangeToPercent = (val)  => { return ( (val + 1) / 2) * 100 + '%' }

                linearGradient.selectAll("stop")
                .data([
                    {offset: rangeToPercent(-1), color: "#4A148C"},
                    {offset: rangeToPercent(-0.85), color: "#AB47BC"},
                    {offset: rangeToPercent(0), color: "white"},
                    {offset: rangeToPercent(0.85), color: "#42A5F5"},
                    {offset: rangeToPercent(1), color: "#0D47A1"},
                ])
                .enter().append("stop")
                .attr("offset", function(d) { return d.offset; })
                .attr("stop-color", function(d) { return d.color; });         
                const legend = svg.append("g")
                legend.append("rect")
                    .attr("x", 125).attr("y", -60)
                    .attr("width", 400)
                    .attr("height", 20)
                    .style("fill", "url(#linear-gradient)");
                legend.append("text").text(-1).attr("x", 120).attr("y", -25)
                legend.append("text").text(0).attr("x", 320).attr("y", -25)
                legend.append("text").text(1).attr("x", 520).attr("y", -25)


                                                         



                
                // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
                const myGroups = Array.from(new Set(data.map(d => d.group)))
                const myVars = Array.from(new Set(data.map(d => d.variable)))
                
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
                
                // Build color scale

                    const colorScale = d3.scaleLinear().domain([-1,-0.85, 0, 0.85, 1])
                    .range(["#4A148C", "#AB47BC", "white", "#42A5F5",  "#0D47A1"])




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
                    .style("stroke", "black")
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






        }
    }
}


</script>