<template>
  <div>

    <v-row>
      <v-col cols="6">
        <div class="overline text-center">
          Relative Contributions of Selected Features
        </div>
        <apexchart :key="relativeGraphKey" type="donut" :options="relativeGraphOptions" :series="relativeGraphSeries"></apexchart>
      </v-col>
      <v-col cols="6">
        <div class="overline text-center">
          Total Contributions to All Features
        </div>
        <apexchart :key="totalGraphKey" type="donut" :options="totalGraphOptions" :series="totalGraphSeries"></apexchart>
      </v-col>
    </v-row>

  </div>


</template>
<script>
export default {
  name: 'FeatureSelectorDonutGraphs',
  props: [
    'input',
  ],
  data() {
    return {
      //Relative Graph
      relativeGraphKey: 0,
      relativeGraphOptions: null, //set by created method
      relativeGraphSeries: [],
      //Total Graph
      totalGraphKey: 0,
      totalGraphOptions: null,
      totalGraphSeries: []
    }
  },
  watch: {
    input() {
      this.makeRelativeGraph()
      this.makeTotalGraph()
      // { "feature": "worstconcavepoints", "score": 733.3811414895886, "selectedPercentage": 10, "totalPercentage": 10 }

    },

  },
  created() {
    this.relativeGraphOptions = this.makeGraphOptions()
    this.totalGraphOptions = this.makeGraphOptions()
  },

  methods: {
    makeRelativeGraph() {
      this.relativeGraphOptions = this.makeGraphOptions()
      this.relativeGraphOptions.labels = []
      this.relativeGraphSeries = []
      let otherSum = 0
      this.input.forEach((item, index) => {
        if (index < 9) {
          this.relativeGraphSeries.push(item.selectedPercentage)
          this.relativeGraphOptions.labels.push(item.feature)
        }
        else {
          otherSum += item.selectedPercentage
        }
      })
      if (otherSum > 0) {
        this.relativeGraphSeries.push(otherSum)
        this.relativeGraphOptions.labels.push('other feature (see table)')
      }
      this.relativeGraphKey += 1
    },
    makeTotalGraph() {
      this.totalGraphOptions = this.makeGraphOptions()
      this.totalGraphOptions.labels = []
      this.totalGraphSeries = []
      let unused = 100
      let otherSum = 0
      this.input.forEach((item, index) => {

        unused -= item.totalPercentage

        if (index < 9) {
          this.totalGraphSeries.push(item.totalPercentage)
          this.totalGraphOptions.labels.push(item.feature)
        }
        else {
          otherSum += item.totalPercentage
        }
      })
      if (otherSum > 0) {
        this.totalGraphSeries.push(otherSum)
        this.totalGraphOptions.labels.push('other feature (see table)')
      }
      this.totalGraphOptions.colors = this.totalGraphOptions.colors.slice(0,this.totalGraphOptions.labels.length)

      this.totalGraphSeries.push(unused)
      this.totalGraphOptions.labels.push('unused features')

      this.totalGraphOptions.colors.push('#D3D3D3')


      this.totalGraphKey += 1

    },
    makeGraphOptions() {
      return {
        colors: [
          '#4c86ff',
          '#577df9',
          '#6173f3',
          '#6b69ec',
          '#745ee4',
          '#7d53db',
          '#8446d2',
          '#8b38c8',
          '#9225bd',
          '#9229b1',
        ],
        labels: [],
        chart: {
          animations: {
            enabled: true
          }
        },

        dataLabels: {
          enabled: false
        },

        plotOptions: {
        }
      }
    },
  }

}
</script>
<style>

</style>
