<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent v-if="filePipeline && filePipeline.columnAdjust != null">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <div v-if="totalMissingRows > 0">
      <div class="my-5" v-for="(count, file) in filePipeline.columnAdjust.nan_rows" :key="file">
        <div class="overline primary--text">{{file}}</div>
        <div class="ml-3">
          {{count}} row<span v-if="count > 1 || count == 0">s</span> with missing values 
          <div>{{Object.keys(filePipeline.columnAdjust.nan_columns[file]).length}} columns with missing values</div>
          <div class="pl-5" v-for="(val, col) in filePipeline.columnAdjust.nan_columns[file]" :key="col">
          {{col}}: {{val}}
          </div>
        </div>
      </div>
      <div class="overline purple--text">Missing Row Options</div>
      <v-alert dense color="purple" text v-if="manyMissingRows">
        One or more files has >= {{maxMissingPercent}}% rows with missing values. We do not recommend using imputation.
      </v-alert>
      <v-radio-group
        class="mt-0"
        v-model="filePipeline.rowOption"
      >
        <v-radio label="Remove rows with missing data" value="0"></v-radio>
        <v-radio label="Impute rows with missing data" value="1"></v-radio>
      </v-radio-group>
      <v-switch class="mt-2 right" label="Include indexs in export" v-model="includeIndexes"></v-switch>
    </div>
    <div v-else>
      <v-icon color="green" >mdi-check-circle</v-icon> No missing rows.
    </div>
    
    <div class="text-right">
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
      let rows = this.filePipeline.columnAdjust.nan_rows
      for (let row in rows) {
        total += rows[row]
      }
      return total
    }
  },
  methods: {
    processStep() {
      this.filePipeline.handleRows(this.includeIndexes)
      this.$emit('processStep')
    }

      



  }
}
</script>
