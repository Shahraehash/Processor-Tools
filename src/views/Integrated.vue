<template>
    <v-container>
      <MenuBar
        :title="$store.state.tools[$options.name].title"
        :icon="$store.state.tools[$options.name].icon"
        :description="$store.state.tools[$options.name].description"
        @reset="resetStep1"
      />

      <!-- Get data into preprocessor -->
      <pmFileSeed 
        @nextStep="initilizeFiles($event)"
        />
      
      <!-- Determine steps for preprocessing -->
      <pmFileRoute
        :files="steps[0]"
        />

    </v-container>
  
  </template>
  <script>
  //packages

  
  //support code
  
  
  //components
import MenuBar from "@/components/MenuBar.vue";
import pmFileSeed from '@/PreMilo/pmComponents/pmFileSeed.vue'
import pmFileRoute from "../PreMilo/pmComponents/pmFileRoute.vue";

import PreMilo from '@/PreMilo'

  
  export default {
    name: 'Integrated',
    components: {
        MenuBar,
        pmFileSeed,
        pmFileRoute
  
    },
    data() {
        return {
          steps: [],

        }
    },
    computed: {
   
  
    },
    mounted() {
        console.log(PreMilo)
    },
    methods: {
        initilizeFiles(files) {
            this.steps = []
            this.steps.push(files)
        }
  
    }
  
  }
  </script>
  <style>

  
  </style>
  