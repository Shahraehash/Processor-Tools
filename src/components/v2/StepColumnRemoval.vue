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
        <TableMissingDataByColumn :files="filePipeline.files"/>

      </v-col>      
    </v-row>

    <div class="overline purple--text">Column Removal</div>
    <div>Any columns with signficant missing data can be optionally removed.</div>
    <v-row>
      <v-col cols="6">
          <v-combobox
            label="Columns to Remove"
            dense
            outlined
            v-model="columnsToRemove"
            multiple
            :items="Object.keys(filePipeline.files[0].params.nanByColumn)"
          >
          </v-combobox>
      </v-col>
    </v-row>

    

      







    
    <div class="text-right" >
      <v-btn
        @click="$emit('nextStep', columnsToRemove)"
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
import TableMissingDataByColumn from '@/components/TableMissingDataByColumn'

export default {
  name: 'StepColumnRemoval',
  components: {
    StepHeading,
    ApexPlotMissingData,
    TableMissingDataByColumn
  },
  data() {
    return {
      columnsToRemove: [],
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

  }
}
</script>
