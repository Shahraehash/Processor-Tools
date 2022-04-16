<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent>
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <div v-for="(pipeline, index) in filePipelines" :key="index">
      <div v-if="pipeline.metadata">
        <div>
          {{pipeline.metadata.filename}}
        </div>
        <v-card flat outlined class="ma-3 pa-3" v-for="(values, column) in pipeline.metadata.invalid_columns" :key="column">
          <div >
            <span class="title font-weight-medium">{{column}}</span> <span class="grey--text">{{values.length}} values</span>
          </div>
          <div >
            <v-chip v-for="v in values" :key="v">{{v}}</v-chip>
          </div>
        </v-card>        
      </div>
    </div>
    <div class="text-right" >
      <v-btn
        @click="runDummy()"
        class="primary"
        rounded
        text
        dark
        >
        Dummy Encode
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
    'filePipelines',
    'stepNumber',
    'stepTitle',
  ],
  watch: {
    filePipelines() {
      console.log(this.filePipelines)

    }
  },
  methods: {
    runDummy() {
      this.filePipelines.forEach(pipeline => {
        pipeline.dummyEncodeNonNumericColumns()
      })
    }


  }
}
</script>
