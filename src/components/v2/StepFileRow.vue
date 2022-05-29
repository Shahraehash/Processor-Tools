<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent v-if="filePipeline && filePipeline.columnAdjust != null">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <!-- No missing data -->
    <div v-if="totalMissingRows == 0">
      <v-icon color="green" >mdi-check-circle</v-icon> No missing values.
    </div>
    <!-- Missing Rows -->
    <div v-else>
      <!-- Settings -->
      <div>
        <div class="overline purple--text">Missing Value Options</div>
        <v-alert dense color="purple" text v-if="manyMissingRows">
          One or more files has >= {{maxMissingPercent}}% cells with missing values. We do not recommend using imputation.
        </v-alert>
        <v-radio-group
          @change="setRowOption($event)"
          class="mt-0"
          v-model="rowOption"
          >
          <v-radio label="Remove rows with missing data" value="0"></v-radio>
          <v-radio label="Impute cells with missing data" value="1"></v-radio>
        </v-radio-group>
        
      </div>
      <div>
        
      </div>
    </div>


<v-card flat outlined class="pa-3 my-2" v-for="(data, file) in filePipeline.columnAdjust" :key="file">
      <v-row dense >
        <v-col cols="6">
          <v-icon>mdi-update</v-icon>
          {{ file }}
        </v-col>
        <!-- <v-col cols="3">
          <div v-for="(val,col) in JSON.parse(data.original.nanByColumn)" :key="col">{{col}}: {{val}}</div>
        </v-col> -->
        <v-col cols="3">
          <div>Summary of Change</div>
          <div v-if="rowOption == 0">
            <div>
              {{ data.transform.rows}} total rows
            </div>          
            <div>
              {{ data.transform.nanRows}} missing rows
            </div>
            <div>
              {{data.transform.rows - data.transform.nanRows}} remaining rows 
            </div>  
          </div>
          <div v-if="rowOption == 1">
            <div>
              {{ data.transform.valueCells}} cells with values
            </div>
            <div>
              {{ data.transform.nanCells}} cells imputed
            </div>          
          </div>
        

        </v-col>
        <v-col cols="3">
          <div>Columns with Missing</div>
          <div v-for="(val,col) in JSON.parse(data.original.nanByColumn)" :key="col">{{col}}: {{val}}</div>

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
  },  
  computed: {
    manyMissingRows() {
      let moreThanMaxMissing = false
      this.filePipeline.metadata.initialFiles.forEach(file => {
        file.nanPercent > this.maxMissingPercent ? moreThanMaxMissing = true : null
      })
      return moreThanMaxMissing
    },
    totalMissingRows() {
      let total = 0
      let files = this.filePipeline.columnAdjust
      for (let file in files) {
        total += files[file].original.rows
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
    }

      



  }
}
</script>
