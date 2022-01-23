<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent>
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <div v-for="(pipeline, index) in filePipelines" :key="index">
      <div v-if="pipeline.metadata">
        {{pipeline.metadata.filename}}
      </div>
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


  }
}
</script>
