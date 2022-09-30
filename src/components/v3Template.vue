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
        {{crossValidate}}
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
    import { validateFiles } from '@/v3Methods'


  //components
  import StepHeading from '@/components/StepHeading'  
  import v3ButtonNext from './v3ButtonNext.vue'

  export default {
    name: 'pmFileRoute',
    components: {
      StepHeading,
      v3ButtonNext
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
    },
    data() {
      return {
        crossValidate: null

      }
    },
    computed: {
      currentFiles() {
        return this.files[this.stepNumber - 2]
      }
    },
    async mounted() {
      validateFiles(this.currentFiles, this.target).then(r => this.crossValidate = r)
    },
    methods: {
      next() {
        this.$emit('next')
      }
    }
  
  }
  </script>

  