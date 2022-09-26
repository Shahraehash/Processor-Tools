<template>

    <v-card 
      outlined 
      flat 
      class="ma-3 pa-5" 
      >
      <!-- If one file -->
      <div v-if="files.length == 1">
        We'll need to create seperate trianing and testing files from your single dataset.
      </div>
      <div v-if="files.length >= 2">
        We're checking your files for consistent in columns and target.
        <div>
          {{crossValidate}}
        </div>
        
      </div>      

      
    

    </v-card>
  </template>
  <script>
  //packages

  import axios from 'axios'
  //support code
  


  //components


  export default {
    name: 'pmFileRoute',
    components: {
      
    },
    props: {
      files: {
        type: Array,
        default: () => []
      },
      target: {
        type: String,
        default: null
      }
    },
    data() {
      return {
        crossValidate: null

      }
    },

    watch: {

      files() {
        console.log(this.files)
      },
      target() {
        this.validateFiles().then(r => this.crossValidate = r)
      }
    },
    async mounted() {
      console.log(this.files.length)
      console.log(this.target)
      if (this.files.length > 1 && this.target != '') {
        let r = await this.validateFiles()
        this.crossValidate = r
      }
  
    },
    methods: {
      async validateFiles() {

        let json = {
          fileObjectArray: this.files,
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
  <style scoped>
  #indent-text {
      margin-left: 1.8em;
      text-indent: -1.8em;
  }
  </style>
  