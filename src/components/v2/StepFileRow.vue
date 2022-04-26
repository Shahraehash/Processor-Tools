<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent v-if="filePipeline && filePipeline.columnAdjust != null">
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <div v-for="(count, file) in filePipeline.columnAdjust.nan_rows" :key="file">

        {{file}}: {{count}} missing rows
    </div>
    <v-radio-group
      v-model="filePipeline.rowOption"
    >
      <v-radio label="Remove rows with missing data"></v-radio>
      <v-radio label="Impute rows with missing data"></v-radio>
    </v-radio-group>
    <div class="text-right">
        <v-btn
        @click="filePipeline.handleRows()"
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
  name: 'StepFileDrop',
  components: {
    StepHeading
  },
  data() {
    return {
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
  methods: {

      



  }
}
</script>
