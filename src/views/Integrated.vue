<template>
    <v-container>
      <MenuBar
        :title="$store.state.tools[$options.name].title"
        :icon="$store.state.tools[$options.name].icon"
        :description="$store.state.tools[$options.name].description"
      />

      <!-- Dynamically Render Components Base on Need -->
      <component 
        v-for="(c, key) in componentList" 
        :key="key"
        :is="c.name"
        :stepTitle="c.stepTitle"
        :stepNumber="key + 1"
        :files="files"
        @next="c.events.next"
        @update="c.events.update"
        :ref="'step' + c.key"

        ></component>

    </v-container>
  
  </template>
  <script>
  //packages

  
  //support code
  
  
  //components
import MenuBar from "@/components/MenuBar.vue";
import pmFileSeed from '@/PreMilo/pmComponents/pmFileSeed.vue'
import pmFileValidate from "../PreMilo/pmComponents/pmFileValidate.vue";
import testComponent from "../PreMilo/pmComponents/testComponent.vue";

import PreMilo from '@/PreMilo'

  
  export default {
    name: 'Integrated',
    components: {
        MenuBar,
        pmFileSeed,
        pmFileValidate,
        testComponent
  
    },
    data() {
        return {
          steps: [],
          target: null,

          componentList: [
            {
              name: 'pmFileSeed',
              stepTitle: 'File Import',
              events: {
                next: (e) => {console.log('next', e)},
                update: (e) => {console.log('update', e)},
              }
          
            }
          ]

        }
    },
    computed: {
   
  
    },
    mounted() {
        console.log(PreMilo)
    },
    methods: {
      initialStep(d) {
        console.log(d)
      }
    }
  
  }
  </script>
  <style>

  
  </style>
  