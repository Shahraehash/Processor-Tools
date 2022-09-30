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
        {{}}  
      <!-- If one file -->

      <!-- Cross Validation -->
      <div>
        <div class="overline purple--text">Cross-file Validation</div>
        <!-- Single File -->
        <div v-if="files.length == 1">
          <div>
            <v-icon color="green" >mdi-check-circle</v-icon>
            Only single data file
          </div>
        </div>
        <div v-else>
          {{crossValidate}}
        </div>

      </div>
      
    
      



      <div v-if="files.length == 1">
        We'll need to create seperate trianing and testing files from your single dataset.
      </div>
      <div v-if="files.length >= 2">
        We're checking your files for consistent in columns and target.
        <div>
          {{crossValidate}}
        </div>
        
      </div>      
      <div class="text-right" v-if="files.length > 0">
        <v3ButtonNext 
        @next="$emit('next')"
        :disabled="currentStep > stepNumber - 1"
        text="Next Step"
        />
      </div>      

      
    

    </v-card>
  </template>
  <script>
  //packages

  import axios from 'axios'
  //support code
  


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

    watch: {

      files() {
        this.validateFiles().then(r => this.crossValidate = r)
      },
    },
    async mounted() {
      if (this.files.length > 1 && this.target != '') {
        let r = await this.validateFiles()
        this.crossValidate = r
      }
  
    },
    methods: {
      async validateFiles() {

        let json = {
          fileObjectArray: this.files[this.stepNumber - 1].fileMetadata,
          target: this.target
        }

        const response = await axios.post('/preprocessor_api/integrated/validate', json, {
          headers: {
            'Content-Type': 'application/json',
          }
        })
        return response.data
      },         
      
    }
  }
  </script>

  