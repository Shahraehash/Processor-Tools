<template>
    <v-container>
      <MenuBar
        :title="$store.state.tools[$options.name].title"
        :icon="$store.state.tools[$options.name].icon"
        :description="$store.state.tools[$options.name].description"
        @reset="reset()"
      />

      <!-- Dynamically Render Components Base on Need -->


        <component 
          v-for="(c, key) in visibleComponents" 
          :key="key"
          :currentStep="currentStep"
          :is="c.component"
          :subcomponent="c.subcomponent"
          :stepTitle="c.stepTitle"
          :stepNumber="key + 1"
          :files="dataFiles"
          :target="target"
          :analysisObj="c.analysisObj"
          :analysisFunction="c.analysisFunction"
          :transformFunction="c.transformFunction"
          :optional="c.optional"
          @next="c.events.next"
          @update="c.events.update; setStep(key)"
          @removeComponent="removeComponent(key)"
          :ref="'step' + key"
        ></component>







      <div class="text-center mt-10" v-if="componentList.length == currentStep">
        <div>Additional Steps</div>
          <v-row justify="center">
            <v-col cols="4" v-for="(item, key) in optional" :key="key">
              <v-card outlined @click="addComponent(item.component)" :disabled="item.disabled">
                <div class="overline">{{item.title}}</div>
                <v-icon x-large :color="item.icon == 'mdi-export' ? 'primary' : ''">{{item.icon}}</v-icon>
              </v-card>          
            </v-col>
          </v-row>

      
      </div>
      <div class="ma-5 white--text">x</div>
      <div class="footer">
        <div class="text-center">Step: {{currentStep + 1}} of {{componentList.length}}</div>

        <v-progress-linear 
          :value="(currentStep + 1) / (componentList.length) * 100"
          :height="10"
          ></v-progress-linear>

      </div>

    </v-container>
  
  </template>
  <script>
  //packages

  
  //support code
  import { 
    transformFileArray,
    analyzeFileArray,
   } from '@/v3Methods'
  
  //components
import MenuBar from "@/components/MenuBar.vue";
import v3FileUpload from "../components/v3FileUpload.vue";
import v3parentStepTemplate from "../components/v3parentStepTemplate.vue";
import V3miniExport from '../components/v3miniExport.vue';



  
  export default {
    name: 'Integrated',
    components: {
    MenuBar,
    v3FileUpload,
    v3parentStepTemplate,
    V3miniExport
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
          optional: [
            {
              'title': 'Multicollinearity Assessment & Removal',
              'icon': 'mdi-chart-bell-curve-cumulative',
              'component': this.getExportComponent(),
              disabled: true
            },    
            {
              'title': 'Feature Selector',
              'icon': 'mdi-select-all',
              'component': this.getExportComponent(),
              disabled: true
            },                          
            {
              'title': 'Finalize Files',
              'icon': 'mdi-export',
              'component': this.getExportComponent(),
              disabled: false
            },    
               
          ]
        }
    },

    mounted() {
        this.componentList = this.getComponentList()
    },
    methods: {
      exportComponent() {
        this.componentList.push(
          {
              component: 'v3testComponentVue',
              stepTitle: 'Ouptut Validation',
              events: {
                next: (e) => { this.nextStep(e);},
                update: (e) => {console.log('update', e); },
              }
          },      
        )
        this.currentStep = this.componentList.length
      },
      addComponent(component) {
        this.componentList.push(component)
      },
      removeComponent(index) {
        this.componentList.splice(index, 1)
        this.currentStep = this.componentList.length
      },

      getExportComponent() {
        return{
          component: 'v3parentStepTemplate',
          subcomponent: 'v3subFinalize',
          stepTitle: 'Export Files for Use in Milo',
          optional: true,
          analysisFunction: analyzeFileArray,
          analysisObj: {method: 'export'},
          transformFunction: transformFileArray,
          events: {
            next: (fileMetadata) => { this.nextStep(fileMetadata);},
            update: (e) => {console.log('update', e); },
          }
        }  
      },

      getComponentList() {
        return [
          {
              component: 'v3FileUpload',
              stepTitle: 'File Import',
              optional: false,
              events: {
                next: (e) => { this.nextStep(e.fileMetadata); this.target = e.target},
                update: (e) => {console.log('update', e); },
              }
          },
          {
              component: 'v3parentStepTemplate',
              subcomponent: 'v3subFileValidate',
              stepTitle: 'File Validation',
              optional: false,
              analysisFunction: analyzeFileArray,
              analysisObj: {method: 'file_validate'},
              transformFunction: transformFileArray,
              events: {
                next: (fileMetadata) => { this.nextStep(fileMetadata);},
                update: (e) => {console.log('update', e); },
              }
          },   
          {
              component: 'v3parentStepTemplate',
              subcomponent: 'v3subColumnRemoval',
              stepTitle: 'Column Pruning to Minimize Missing Data',
              optional: false,
              analysisFunction: analyzeFileArray,
              analysisObj: {method: 'column_removal'},
              transformFunction: transformFileArray,
              events: {
                next: (fileMetadata) => { this.nextStep(fileMetadata);},
                update: (e) => {console.log('update', e); },
              }
          },
          {
              component: 'v3parentStepTemplate',
              subcomponent: 'v3subEncodeNonnumeric',
              stepTitle: 'Ensure all columns are numeric',
              optional: false,
              analysisFunction: analyzeFileArray,
              analysisObj: {method: 'encode_nonnumeric'},
              transformFunction: transformFileArray,
              events: {
                next: (fileMetadata) => { this.nextStep(fileMetadata);},
                update: (e) => {console.log('update', e); },
              }
          },  
          {
              component: 'v3parentStepTemplate',
              subcomponent: 'v3subTrainTestSplit',
              stepTitle: 'Allocate Data for Training and Testing',
              optional: false,
              analysisFunction: analyzeFileArray,
              analysisObj: {method: 'train_test_split_impute'},
              transformFunction: transformFileArray,
              events: {
                next: (fileMetadata) => { this.nextStep(fileMetadata);},
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
      nextStep(fileMetadata) {
        this.dataFiles.push(fileMetadata)
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
  <style scoped>
  .footer {
      position: fixed;
      bottom: 0;
      left: 50%;
      transform: translate(-50%, 0);
      width: 100%;
      background: white;
  }

    

  
  </style>
  