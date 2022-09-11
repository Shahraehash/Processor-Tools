<template>
    <v-container>
      <MenuBar
        :title="$store.state.tools[$options.name].title"
        :icon="$store.state.tools[$options.name].icon"
        :description="$store.state.tools[$options.name].description"
        @reset="resetStep1"
      />
    </v-container>
  
  </template>
  <script>
  //packages

  
  //support code
  
  
  //components
import MenuBar from "@/components/MenuBar.vue";

import MI from '@/ModuleIntegrated'

  
  export default {
    name: 'Integrated',
    components: {
        MenuBar
  
    },
    data() {
        return {

        }
    },
    computed: {
   
  
    },
    mounted() {
        console.log(MI)
    },
    methods: {
  
    }
  
  }
  </script>
  <style>

  
  </style>
  