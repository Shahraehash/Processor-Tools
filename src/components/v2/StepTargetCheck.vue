<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent>
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    /> 
    <div v-for="(file, index) in filePipeline.metadata.initialFiles" :key="index">
        <div>{{file.name}}: {{index}}</div>
        <div>{{file.targetValidation}}</div>
    </div>

  </v-card>
</template>
<script>
//packages


//support code

//components
import StepHeading from '@/components/StepHeading'

export default {
  name: 'StepTargetCheck',
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

  },
  methods: {

  }
}
</script>
