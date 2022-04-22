<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent>
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <div>
      Pipeline ID: {{filePipeline.metadata.pipelineId}}
    </div>
    <v-card outlined class="ma-3 pa-3" v-for="(file, key) in filePipeline.metadata.initialFiles" :key="key">
    <div>{{file.name}}</div>    
    <div>Columns: {{file.columns}}</div>  
    <div>Rows: {{file.Rows}}</div>    
    <div>Column Names: {{file.columnNames}}</div>    
    <div>Invalid Column Adjustments</div>    
    <div v-for="(comment, col) in file.invalidColumnsComments" :key="col">
      {{col}} : {{comment}}
    </div>    
    </v-card>  



    <!-- <div class="text-right" >
      <v-btn
        @click="runDummy()"
        class="primary"
        rounded
        text
        dark
        >
        Dummy Encode
      </v-btn>
    </div>     -->

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
