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

//  import axios from 'axios'
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
      }
    },
    data() {
      return {

      }
    },

    watch: {

      files() {
        console.log(this.files)
      }
    },
    mounted() {
  
    },
    methods: {


    }
  }
  </script>
  <style scoped>
  #indent-text {
      margin-left: 1.8em;
      text-indent: -1.8em;
  }
  </style>
  