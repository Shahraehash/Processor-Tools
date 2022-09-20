<template>
    <v-container>
      <MenuBar
        :title="$store.state.tools[$options.name].title"
        :icon="$store.state.tools[$options.name].icon"
        :description="$store.state.tools[$options.name].description"
        @reset="resetStep1"
      />

      <pmFileSeed />

    </v-container>
  
  </template>
  <script>
  //packages

  
  //support code
  
  
  //components
import MenuBar from "@/components/MenuBar.vue";
import pmFileSeed from '@/PreMilo/pmComponents/pmFileSeed.vue'

import PreMilo from '@/PreMilo'

  
  export default {
    name: 'Integrated',
    components: {
        MenuBar,
        pmFileSeed
  
    },
    data() {
        return {

        }
    },
    computed: {
   
  
    },
    mounted() {
        console.log(PreMilo)
    },
    methods: {
  
    }
  
  }
  </script>
  <style>

  
  </style>
  