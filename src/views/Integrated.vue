<template>
    <v-container>
      <MenuBar
        :title="$store.state.tools[$options.name].title"
        :icon="$store.state.tools[$options.name].icon"
        :description="$store.state.tools[$options.name].description"
        @reset="reset()"
      />
      {{dataFiles.length}}
      {{currentStep}}

      <!-- Dynamically Render Components Base on Need -->
      <component 
        v-for="(c, key) in visibleComponents" 
        :key="key"
        :currentStep="currentStep"
        :is="c.name"
        :stepTitle="c.stepTitle"
        :stepNumber="key + 1"
        :files="dataFiles"
        :target="target"
        @next="c.events.next"
        @update="c.events.update; setStep(key)"
        :ref="'step' + key"

        ></component>

      <div class="text-center mt-10" v-if="componentList.length == currentStep">
        Additional optoins
        <div>
          <v-btn @click="exportComponent">Export</v-btn>
        </div>

          <v-row justify="center">
            <v-col cols="3">
              <v-card outlined>
                Additioanl Step

              </v-card>          

            </v-col>
            <v-col cols="3">
              <v-card outlined>
                Additioanl Step

              </v-card>          

            </v-col>
            <v-col cols="3">
              <v-card outlined>
                Additioanl Step

              </v-card>          

            </v-col>                        
          </v-row>

        
      </div>

    </v-container>
  
  </template>
  <script>
  //packages

  
  //support code
  
  
  //components
import MenuBar from "@/components/MenuBar.vue";
import v3FileUploadVue from "../components/v3FileUpload.vue";
import v3FileValidateVue from "../components/v3FileValidate.vue";
import v3testComponentVue from "../components/v3testComponent.vue";
import PreMilo from '@/PreMilo'


  
  export default {
    name: 'Integrated',
    components: {
        MenuBar,
        v3FileUploadVue,
        v3FileValidateVue,
        v3testComponentVue
  
    },
    computed: {
      currentDataFiles() {
        this.refreshKey
        let currentIndex = this.dataFiles.length - 1
        return this.dataFiles[currentIndex]
      },
      visibleComponents() {
        return this.componentList.filter((item, index) => {
          item
          return index <= this.currentStep
        })
      }
    },
    data() {
        return {
          currentStep: 0,
          dataFiles: [],
          target: null,
          refreshKey: 0,

          componentList: [],

        }
    },

    mounted() {
        console.log(PreMilo)
        this.componentList = this.getComponentList()
    },
    methods: {
      exportComponent() {
        this.componentList.push(
          {
              name: 'v3testComponentVue',
              stepTitle: 'Ouptut Validation',
              events: {
                next: (e) => { this.nextStep(e);},
                update: (e) => {console.log('update', e); },
              }
          },      
        )
        this.currentStep = this.componentList.length
      },

      getComponentList() {
        return [
          {
              name: 'v3FileUploadVue',
              stepTitle: 'File Import',
              events: {
                next: (e) => { this.nextStep(e); this.target = e.target},
                update: (e) => {console.log('update', e); },
              }
          
          },
          {
              name: 'v3FileValidateVue',
              stepTitle: 'File Validation',
              events: {
                next: (e) => { this.nextStep(e);},
                update: (e) => {console.log('update', e); },
              }
          },              
              

          ]
      },
      reset() {
        this.currentStep = 0
      },
      initialStep(d) {
        console.log(d)
      },
      nextStep(e) {
        this.dataFiles.push(e)
        this.currentStep++
      },
      setStep(step) {
        this.currentStep = step
        this.dataFiles.length = step //remove all data after step
        this.refreshKey++ //needs to trigger computed property for currentDataFiles
      }
    }
  
  }
  </script>
  <style>

  
  </style>
  