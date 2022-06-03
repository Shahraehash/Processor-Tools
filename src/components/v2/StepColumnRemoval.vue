<template>


  <v-card outlined flat class="ma-3 pa-5">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />

      <v-row>
        <v-col cols="6">
          <ApexPlotMissingData :files="filePipeline.files"/>
        </v-col>
        <v-col cols="6" >
          <v-data-table
            :headers="headers"
          ></v-data-table>
        </v-col>      
      </v-row>      







    
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
import ApexPlotMissingData from '@/components/ApexPlotMissingData'

export default {
  name: 'StepColumnRemoval',
  components: {
    StepHeading,
    ApexPlotMissingData
  },
  data() {
    return {
      headers: [
          {
            text: 'Column',
            align: 'start',
            sortable: false,
            value: 'column',
          },   
          {
            text: 'Missing Value Count',
            align: 'start',
            sortable: false,
            value: 'count',
          },                  
      ],
      tableData: null


    }
  },
  props: [
    'filePipeline',
    'stepNumber',
    'stepTitle',
    'disableNext'
  ],
  watch: {

  },
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
 
  },  
  methods: {
    generateMissingDataTable(data) {
      let tableData = []
      for (let key in data) {
        tableData.push({
          column: key,
          count: data[key]
        })
      }
      return tableData
    },
  }
}
</script>
