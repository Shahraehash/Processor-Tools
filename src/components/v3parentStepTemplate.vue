<template>

  <v-card 
    flat 
    class="ma-3 pa-5" 
    >
    
    <!-- Heading -->



        <v3StepHeading
        style="display: inline-flex;"
        :stepNumber="stepNumber"
        :stepTitle="stepTitle"
        />

        <v3miniExport :currentFiles="currentFiles" class="mt-n13"/>

        <v-spacer></v-spacer>

        <v-btn @click="$emit('removeComponent')" class="float-right" text v-if="optional" style="display: inline-flex;">
          Remove Step
          <v-icon >mdi-close</v-icon>
        </v-btn>  
        


    <div>

      <v-spacer></v-spacer>

    <v-divider class="mb-5"></v-divider>  
    </div>
  
    


    
    <!-- EXPORT -->


    <!-- Core Component -->
    <div>
      <transition appear name="fade" tag="div">

        <v-component 
          v-if="analysis"
          :is="subcomponent" 
          :currentFiles="currentFiles" 
          :analysis="analysis" 
          :target="target"
          :files="files"
          @update="update($event)"
          >
        </v-component>
        <div v-else class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
          class="mt-5"
          ></v-progress-circular>
          <v-alert
            class="mt-5"
            color="primary"
            text
            dense
            v-if="longProcessTimeAlert"
            >
            Larger datasets can take much longer to process.
          </v-alert>
        </div>
      </transition>

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
import v3subMulticolinearity from './v3subMulticolinearity.vue'


export default {
  name: 'v3parentStepTemplate',
  components: {
    v3StepHeading,
    v3ButtonNext,
    v3miniExport,
    v3subFileValidate,
    v3subColumnRemoval,
    v3subEncodeNonnumeric,
    v3subTrainTestSplit,
    v3subMulticolinearity
  },
  props: {
    stepNumber: {
      type: Number || String
    },
    stepTitle: {
      type: String
    },
    optional: {
      type: Boolean,
      default: false
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
      longProcessTimeAlert: false,
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
      let r = await this.analysisFunction(this.currentFiles, this.target, this.analysisObj)
      let delay = (ms) => new Promise(res => setTimeout(res, ms));
      await delay(500)
      this.longProcessTimeClock()
      this.analysis = r
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
    },
    async longProcessTimeClock() {
      this.longProcessTimeAlert = false
      let delay = (ms) => new Promise(res => setTimeout(res, ms));
      await delay(5000)
      this.longProcessTimeAlert = true
    }
  }

}
</script>

<style scoped>
  .fade-enter-active {
  transition: opacity .5s;
}
.fade-leave-active {
  transition: opacity 0s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>

