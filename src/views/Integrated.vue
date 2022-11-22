<template>
    <v-container>
      <MenuBar
        :title="$store.state.tools[$options.name].title"
        :icon="$store.state.tools[$options.name].icon"
        :description="$store.state.tools[$options.name].description"
        @reset="reset()"
      />

      <!-- Dynamically Render Components Base on Need -->

      <transition-group appear name="fade" tag="div" >
      
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
      </transition-group>


      <!-- Additional Step Selection -->
      <transition appear name="fade" tag="div">
        <div class="text-center mt-10" v-if="componentList.length == currentStep">
        <v3miniAdditionalSteps
          :componentList="componentList"
          :optionalComponents="optionalComponents" 
          @addComponent="addComponent($event)"
          />


      </div>        

      </transition>





      <div class="ma-5 white--text">x</div>
      <div class="footer" v-if="progressBarData.show">
        <div class="text-center text-h7 primary--text">Step: {{progressBarData.current}} of {{progressBarData.total}}</div>

        <v-progress-linear 
          :value="progressBarData.percentage"
          :height="15"
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
import v3Finalize from '../components/v3Finalize.vue';
import V3miniExport from '../components/v3miniExport.vue';
import v3miniAdditionalSteps from '../components/v3miniAdditionalSteps.vue';


  
  export default {
    name: 'Integrated',
    components: {
    MenuBar,
    v3FileUpload,
    v3parentStepTemplate,
    v3Finalize,
    V3miniExport,
    v3miniAdditionalSteps
    },
    computed: {
      progressBarData() {
        let progress = {
          show: false,
          current: 0,
          total: 0,
          percentage: 0,
        }
        if (this.componentList.length > 0) {
          progress.show = true
          progress.current = this.currentStep + 1
          let filteredList = this.componentList.filter((item) => {
            return item.component != 'v3Finalize'
          })
          progress.total = filteredList.length + 1
          progress.percentage = (progress.current / progress.total) * 100
        }


        return progress
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
          optionalComponents: [
            {
              'title': 'Multicollinearity Evaluation',
              'icon': 'mdi-chart-bell-curve-cumulative',
              'component': this.getMulticolinearityComponent(),
              disabled: false
            },    
            // {
            //   'title': 'Feature Selector',
            //   'icon': 'mdi-select-all',
            //   'component': this.getExportComponent(),
            //   disabled: true
            // },                          
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
        this.componentList.splice(index, this.componentList.length - index)
        this.currentStep = this.componentList.length
      },

      getExportComponent() {
        return{
          component: 'v3Finalize',
          stepTitle: 'Finalize Files for Use in Milo',
          optional: true,
          files: this.dataFiles,
          analysisFunction: analyzeFileArray,
          analysisObj: {method: 'export'},
          
          events: {
            next: (fileMetadata) => { this.nextStep(fileMetadata);},
            update: (e) => {console.log('update', e); },
          }
        }  
      },
      getMulticolinearityComponent() {
        return {
          component: 'v3parentStepTemplate',
          subcomponent: 'v3subMulticolinearity',
          stepTitle: 'Assess for and Remove Multicolinearity',
          optional: true,
          analysisFunction: analyzeFileArray,
          analysisObj: {method: 'multicolinearity'},
          transformFunction: transformFileArray,
          events: {
            next: (fileMetadata) => { this.nextStep(fileMetadata);},
            update: (e) => {console.log('update', e); },
          },
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
              },
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
              },
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
              },
          },
          {
              component: 'v3parentStepTemplate',
              subcomponent: 'v3subEncodeNonnumeric',
              stepTitle: 'Convert non-numeric columns to numeric representations',
              optional: false,
              analysisFunction: analyzeFileArray,
              analysisObj: {method: 'encode_nonnumeric'},
              transformFunction: transformFileArray,
              events: {
                next: (fileMetadata) => { this.nextStep(fileMetadata);},
                update: (e) => {console.log('update', e); },
              },
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
              },
          },                                             
              

          ]
      },
      reset() {
        console.log('reset')
        console.log(this.$refs.step0)
        this.$refs.step0[0].resetComponent() // all other components will be reset by v-if/v-for rendering
        this.currentStep = 0
        this.dataFiles = []
        this.target = null
        this.refreshKey = 0
        this.componentList = this.getComponentList()
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

  .fade-enter-active {
  transition: opacity .5s;
}
.fade-leave-active {
  transition: opacity .3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}

  
  </style>
  