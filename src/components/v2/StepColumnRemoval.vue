<template>


  <v-card outlined flat class="ma-3 pa-5">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <apexchart width="500" type="bar" :options="options" :series="series"></apexchart>
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
      }]        

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
      console.log(this.filePipeline)

    }
  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
  },  
  methods: {

  }
}
</script>
