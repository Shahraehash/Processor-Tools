<template>


  <v-card outlined flat class="ma-3 pa-5">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <!-- No missing data -->
    <div v-if="columnsPossibleToRemove.length == 0">
      <v-icon color="green" >mdi-check-circle</v-icon> No missing values.
    </div>
    <!-- Missing Rows -->    
    <div v-else>
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
              :items="columnsPossibleToRemove"
              @change="$emit('changeColumnRemoval')"
            >
            </v-combobox>
        </v-col>
      </v-row>      
    </div>

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
import _ from 'underscore'
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
  computed: {
    columnsPossibleToRemove() {
      if (this.filePipeline) {
        let columns = []
        this.filePipeline.files.forEach(file => {
          columns = columns.concat(Object.keys(file.params.nanByColumn))
        })
        return _.uniq(columns)
      }
      else {
        return []
      }      

    }
  },
  methods: {

  }
}
</script>
