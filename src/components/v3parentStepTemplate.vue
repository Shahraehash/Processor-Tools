<template>

  <v-card 
    flat 
    class="ma-3 pa-5" 
    >
    <v-divider class="mb-5"></v-divider>
    <!-- Heading -->
    <v3StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
      />    
    <v3miniExport :currentFiles="currentFiles" class="mt-n15"  @manualUpdate="$emit('update')"/>
    
    <!-- EXPORT -->


    <!-- Core Component -->
    <div>
      <v-component 
        v-if="analysis"
        :is="subcomponent" 
        :currentFiles="currentFiles" 
        :analysis="analysis" 
        :target="target"
        @update="update($event)"
        >
      </v-component>
    </div>
    <!-- Action Button -->
    <div class="text-right" v-if="files.length > 0">
      <v3ButtonNext 
      @next="next"
      :disabled="currentStep > stepNumber - 1 || !complete"
      text="Next"
      />

    </div>      
  </v-card>
</template>
<script>
//packages

//support code


//components
import v3StepHeading from '@/components/v3StepHeading'  
import v3ButtonNext from './v3ButtonNext.vue'
import v3miniExport from './v3miniExport.vue'

//subcomponents
import v3subFileValidate from './v3subFileValidate'
import v3subColumnRemoval from './v3subColumnRemoval.vue'
import v3subEncodeNonnumeric from './v3subEncodeNonnumeric.vue'
import v3subTrainTestSplit from './v3subTrainTestSplit.vue'


export default {
  name: 'v3parentStepTemplate',
  components: {
    v3StepHeading,
    v3ButtonNext,
    v3miniExport,
    v3subFileValidate,
    v3subColumnRemoval,
    v3subEncodeNonnumeric,
    v3subTrainTestSplit
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
    analysisObj: {
      type: Object,
      default: () => {}
    },    
    transformFunction: {
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
      complete: true,
      transformObj: null,

    }
  },
  computed: {
    currentFiles() {
      return this.files[this.stepNumber - 2]
    }
  },
  async mounted() {
    window.scrollTo(0,document.body.scrollHeight);
    if (this.analysisFunction != null) {
      this.analysisFunction(this.currentFiles, this.target, this.analysisObj)
      .then(r => this.analysis = r)
    }
    
  },
  methods: {
    next() {
      this.transformFunction(this.currentFiles, this.target, this.transformObj)
      .then(r => this.$emit('next', r))
    },
    update(obj) {
      this.complete = obj.complete
      this.transformObj = obj.transformObj
      this.$emit('update')
    }
  }

}
</script>

