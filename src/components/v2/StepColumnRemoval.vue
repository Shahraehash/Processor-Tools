<template>


  <v-card outlined flat class="ma-3 pa-5">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    {{}}
    <apexchart :key="redraw" width="500" type="bar" :options="options" :series="series"></apexchart>
    <div class="text-right" >
      <v-btn
        @click="$emit(nextStep)"
        class="primary"
        :disabled="disableNext"
        rounded
        text
        dark
        >
        Next Step
      </v-btn>
    </div>    

  </v-card>
</template>
<script>
//packages

//support code

//components
import StepHeading from '@/components/StepHeading'

export default {
  name: 'StepColumnRemoval',
  components: {
    StepHeading
  },
  data() {
    return {
      options: {
        chart: {
          id: 'vuechart-example'
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
        }
      },
      series: [{
        name: 'series-1',
        data: [30, 40, 45, 50, 49, 60, 70, 91]
      }],
      redraw: 0,  

    }
  },
  props: [
    'filePipeline',
    'stepNumber',
    'stepTitle',
    'disableNext'
  ],
  watch: {
    filePipeline() {

    }
  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
          let f = this.filePipeline.metadata.files[0].params.nanByColumnPercent
      this.options.xaxis.categories = Object.keys(f)
      this.series[0].data = Object.values(f)
      this.redraw += 1
  },  
  methods: {

  }
}
</script>
