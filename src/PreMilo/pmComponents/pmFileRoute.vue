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
        We need to check your data for consistency.
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

      }
    },

    watch: {

      files() {
        console.log(this.files)
      },
      taget() {
        console.log(this.target)
        this.crossValidateFiles()
      }
    },
    async mounted() {
      console.log(this.files.length)
      console.log(this.target)
      if (this.files.length > 1 && this.target != '') {
        let r = await this.crossValidateFiles()

      }
  
    },
    methods: {
      async crossValidateFiles() {

        let json = {
          fileObjectArray: this.files,
          target: this.target
        }

        const response = await axios.post('/preprocessor_api/integrated/crossvalidate', json, {
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
  