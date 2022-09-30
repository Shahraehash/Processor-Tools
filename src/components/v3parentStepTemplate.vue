<template>

  <v-card 
    outlined 
    flat 
    class="ma-3 pa-5" 
    >
    <!-- Heading -->
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
      />         

    <!-- Core Component -->
    <div>
      <v-component 
        v-if="analysis"
        :is="subcomponent" 
        :currentFiles="currentFiles" 
        :analysis="analysis" 
        :target="target">
      </v-component>
    </div>
  
    <!-- Action Button -->
    <div class="text-right" v-if="files.length > 0">
      <v3ButtonNext 
      @next="next"
      :disabled="currentStep > stepNumber - 1"
      text="Next"
      />
    </div>      
  </v-card>
</template>
<script>
//packages

//support code



//components
import StepHeading from '@/components/StepHeading'  
import v3ButtonNext from './v3ButtonNext.vue'

//subcomponents
import v3subFileValidate from './v3subFileValidate'


export default {
  name: 'v3parentStepTemplate',
  components: {
    StepHeading,
    v3ButtonNext,
    v3subFileValidate
  },
  props: {
    stepNumber: {
      type: Number
    },
    stepTitle: {
      type: String
    },
    files: {
      type: Array,
      default: () => []
    },
    target: {
      type: String,
      default: null
    },
    currentStep: {
      type: Number
    },
    subcomponent: {
      type: String,
      default: null
    },
    analysisFunction: {
      type: Function,
      default: null
    },
  },
  data() {
    return {
      loading: false,
      loadingButton: false,
      //
      analysis: null,

    }
  },
  computed: {
    currentFiles() {
      return this.files[this.stepNumber - 2]
    }
  },
  async mounted() {
    if (this.analysisFunction != null) {
      this.analysisFunction(this.currentFiles, this.target).then(r => this.analysis = r)
    }
    
  },
  methods: {
    next() {
      this.$emit('next')
    }
  }

}
</script>

