<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent v-if="filePipeline && filePipeline.columnAdjust != null">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <div v-if="totalMissingRows > 0">
      <div class="my-5" v-for="(count, file) in filePipeline.columnAdjust.nan_rows" :key="file">
        <div class="overline primary--text">{{file}}</div>
        {{count}} row<span v-if="count > 1 || count == 0">s</span> with missing values 
      </div>
      <v-radio-group
        v-model="filePipeline.rowOption"
      >
        <v-radio label="Remove rows with missing data"></v-radio>
        <v-radio label="Impute rows with missing data"></v-radio>
        <v-switch class="right" label="Include indexs in export" v-model="includeIndexes"></v-switch>
      </v-radio-group>
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
      includeIndexes: false
    }
  },
  props: [
    'filePipeline',
    'stepNumber',
    'stepTitle',
  ],
  watch: {
    filePipeline() {
      console.log(this.filePipeline)

    }
  },
  computed: {
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
