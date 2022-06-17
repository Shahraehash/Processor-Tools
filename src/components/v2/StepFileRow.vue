<template>


  <v-card outlined flat class="ma-3 pa-5" >
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <!-- No missing data -->
    <div v-if="totalMissingCells == 0">
      <v-icon color="green" >mdi-check-circle</v-icon> No missing values.
    </div>
    <!-- Missing Rows -->
    <div v-else>
      <!-- Settings -->
      <div>
        <div class="overline purple--text">Missing Value Options</div>
        <v-alert dense color="purple" text v-if="manyMissingRows">
          More than {{maxMissingPercent}}% of cells have missing values. We do not recommend using imputation.
        </v-alert>
        <v-radio-group
          @change="setRowOption($event)"
          class="mt-0"
          v-model="rowOption"
          >
          <v-radio label="Remove rows with missing data" :value="0"></v-radio>
          <v-radio label="Impute cells with missing data" :value="1"></v-radio>
        </v-radio-group>
        
      </div>
      <div>
        
      </div>
    </div>


<v-card flat outlined class="pa-3 my-2" v-for="(data, file) in filePipeline.columnAdjust" :key="file">
      <v-row dense >
        <v-col cols="54">
          <v-icon>mdi-update</v-icon>
          {{ file }}
  
        </v-col>
        <v-col cols="7">
          <div class="overline">Columns</div>
          <div class="title" ml-1>
            {{ data.original.columns}} <v-icon>mdi-arrow-right</v-icon> {{data.transform.columns}}
          </div>
          <div>
            <v-icon color="green" v-if="showDiff(data.transform.columnNames, data.original.columnNames).length > 0">mdi-plus-circle </v-icon>
            <v-chip small outlined v-for="(item, key) in showDiff(data.transform.columnNames, data.original.columnNames)" :key="key" >{{ item }}</v-chip>
          </div>
          <div class="mt-5">
            <v-icon color="red" v-if="showDiff(data.original.columnNames, data.transform.columnNames).length > 0">mdi-minus-circle</v-icon>
            <v-chip small outlined v-for="(item, key) in showDiff(data.original.columnNames, data.transform.columnNames)" :key="key" >{{ item }}</v-chip>
          </div>
          <div class="mt-3 overline">
            Rows
          </div>
          <div class="title ml-1">
          </div>          
            <div v-if="rowOption == 0">
              <div class="title ml-1">
                {{ data.original.rows}} <v-icon>mdi-arrow-right</v-icon> {{data.transform.rows - data.transform.nanRows}}
              </div>              
              <div v-if="data.transform.nanRows > 0">
                <v-icon color="red">mdi-minus-circle</v-icon><span class="ml-2">{{data.transform.nanRows}} rows with missing data removed</span>
              </div>
            </div>
            <div v-if="rowOption == 1">
              <div class="title ml-1">
                {{ data.original.rows}} <v-icon>mdi-arrow-right</v-icon> {{data.transform.rows}}
              </div>              
              <div v-if="data.transform.nanCells >0">
                <v-icon color="green">mdi-plus-circle</v-icon><span class="ml-2">{{data.transform.nanCells}} imputed values added</span>
              </div>
            </div>                
         
          

        </v-col>             
      </v-row>
    </v-card>

    
    <div class="text-right">
        <v-switch class="mt-2 right" label="Include indexs in export" v-model="includeIndexes"></v-switch>    
        <v-btn
        @click="processStep"
        class="primary"
        rounded
        text
        dark
        >
        Finalize Files
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

//Inspired by: https://www.raymondcamden.com/2019/08/08/drag-and-drop-file-upload-in-vuejs
export default {
  name: 'StepFileRow',
  components: {
    StepHeading
  },
  data() {
    return {
      rowOption: 0,
      includeIndexes: false,
      maxMissingPercent: 30
    }
  },
  props: [
    'filePipeline',
    'stepNumber',
    'stepTitle',
  ],
  mounted() {
    window.scrollTo(0,document.body.scrollHeight);
    _
  },  
  computed: {
    manyMissingRows() {
      let moreThanMaxMissing = false
      this.filePipeline.files.forEach(file => {
        file.params.nanPercent > this.maxMissingPercent ? moreThanMaxMissing = true : null
      })
      return moreThanMaxMissing
    },
    totalMissingCells() {
      let total = 0
      let files = this.filePipeline.columnAdjust
      for (let file in files) {
        total += files[file].transform.nanCells
      }
      return total
    }
  },
  methods: {
    setRowOption(option) {
      this.filePipeline.setRowOption(option)
    },
    processStep() {
      this.filePipeline.handleRows(this.includeIndexes)
      this.$emit('processStep')
    },
    showDiff(array1, array2) {
      return _.difference(array1,array2)
    }

      



  }
}
</script>
