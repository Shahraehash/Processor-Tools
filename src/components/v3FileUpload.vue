<template>


    <v-card 

      flat 
      class="ma-3 pa-5" 
      @drop.prevent="addFile" 
      @dragover.prevent
      >
      <v3StepHeading
        :stepNumber="stepNumber"
        :stepTitle="stepTitle"
        />      

    <!-- Make Initial Chocie on Approach -->
      <div >
        Let's start by uploading your data. How many files do you have?
      </div>
      <div>
        <v-row>
          <v-col cols="4" v-for="(path, pathKey) in paths" :key="pathKey">
            <v-card 
              v-bind:class="{'path-selection': pathKey == pathSelection, 'path-no-selection': pathKey != pathSelection}" 
              flat 
              class="ma-5 pa-3 text-center"
              @click="setPath(pathKey)"
              >
              <div>
                <v-icon size="35px" :style="pathKey == pathSelection ? 'color: white;' : ''">{{path.icon}}</v-icon>
                <v-icon v-if="path.value == 'train-test'" size="35px" :style="pathKey == pathSelection ? 'color: white;' : ''">{{path.icon}}</v-icon>
              </div>
              <div class="mt-5">{{path.text}}</div>
            </v-card>
          </v-col>
              
          
        </v-row>
      </div>
    <!-- If no files yet -->
      <div 
        v-if="files.length == 0 && pathSelection != null" 
        class="text-center mx-5 mt-5"
        style="border: 4px dashed #d3d3d3; border-radius: 10px; padding: 20px;"
        >
        <div >

          Drag and drop your CSV file<span v-if="allowMultipleFiles">s</span> into this box or click the file icon below to select from systemc dialog.
        </div>
        <div>
          <v-icon 
            size="125" 
            @click="$refs.fileClick.click()" 
            color="grey lighten-1"
            >
            mdi-file-upload-outline
          </v-icon>
        </div>
      </div>
    <!-- Hidden file upload -->
      <input 
        type="file" 
        ref="fileClick" 
        :multiple="allowMultipleFiles" 
        @change="clickAddFile($event)" 
        style="display: none" 
        accept='.csv'
        />

    <!-- If have files -->

      <v-row dense v-if="fileMetadata.length > 0">
        <v-col cols="4"
          v-for="(file, index) in files" 
          
          :key="index"
          >

          <v-card 
      
            flat 
            outlined 
            class="pa-3 my-2 app-file-box-style" 
            >
            

                
                  <v-row>
                    <v-col cols="11">
                      <div style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;">
                        <v-icon>mdi-file</v-icon>
                        {{ file.name }}
                      </div>

                    </v-col>
                    <v-col cols="1" class="ml-n7 mt-n2">
                      <v-btn icon @click="removeFile(file)" title="mdi-close"><v-icon color="primary">mdi-close</v-icon></v-btn>
                    
                    </v-col>

                  </v-row>
                
                
                <div>
                  <v3miniValidate :valid="fileMetadata[index].size.rows > 50" />
                  {{fileMetadata[index].size.rows}} rows
                </div>
                <div>
                  <v3miniValidate :valid="fileMetadata[index].size.cols < 1000" />
                  {{fileMetadata[index].size.cols}} columns
                </div>
                <div>
                  <v3miniValidate :valid="fileMetadata[index].missing.rows == 0" />
                  {{fileMetadata[index].missing.rows}}
                  <span v-if="fileMetadata[index].missing.rows > 0"></span> 
                  rows missing data ({{mxStylePercent(fileMetadata[index].missing.rowsPercent)}}%)
                </div>

                <div>
                  <v-select 
                    v-if="pathSelection == 1"
                    v-model="fileMetadata[index].type" 
                    class="ma-2 mt-7" 
                    label="Data Type" 
                    :items="filteredFileTypes" 
                    outlined
                    item-text="text" 
                    item-value="value"
                    @change="update()"
                    >
                    <template v-slot:selection="{ item, index }">
                      <v-chip class="mt-2" small v-if="index === 0" :color="mxfileTypeColor(item.value)" dark>
                        <span>{{ item.text }}</span>
                      </v-chip>
     
 
                    </template>

                  </v-select>

                </div>
              



          </v-card>          
          
        </v-col>
        <v-col cols="4" v-if="files.length > 0">
          <v-card flat style="margin: 10px; padding: 35px 0;" v-if="showAddFile">
            <div class="text-center mr-3" @click="$refs.fileClick.click()">
            <div class="overline">Add addtional file</div> 
            <v-btn icon
              
              >
              <v-icon large>mdi-plus-circle-outline</v-icon>
              </v-btn>
          </div>

          </v-card>
          <v-alert type="warning" text dense v-if="files.length > 2">You should choose at maximum two files for processing.</v-alert>

        </v-col>

        
      </v-row>
      <div v-if="files.length > 0" class="my-3">
          We will address any <v3miniValidate :valid="false" /> alerts as we progress through the steps.
      </div>

      <v-alert type="warning" v-if="trainTestFilesMatchError">With two data files, you need at least one training and one testing file specified for the data type.</v-alert>
     



  


      <!-- Pick Target -->
      <div class="mt-10" v-if="fileMetadata[0]">
        <div class="my-3">
          Next we need to identify which column in the dataset is the target. This is your dependent variable or the outcome you're trying to predict.
        </div>
        <v-row>
          <v-col cols="6">
            <v-select 
              label="Target Column"
              v-model="target" 
              dense 
              outlined 
              clearable
              :items="fileMetadata[0].names.colsReverse"
              @change="update()"
              ></v-select>          
          </v-col>
        </v-row>
  
      </div>


      <div class="text-right" v-if="files.length > 0">
        <v3ButtonNext 
        @next="next"
        :disabled="!complete"
        text="Next"
        />
      </div>
    </v-card>

  </template>
  <script>
  //packages


  //support code
  import { storeParamFile } from '@/v3Methods'
  import v3Mixin from "@/components/v3Mixin.js";


  //components
  import v3StepHeading from '@/components/v3StepHeading'
  import v3ButtonNext from '@/components/v3ButtonNext'
  import v3miniValidate from './v3miniValidate.vue'

  //Inspired by: https://www.raymondcamden.com/2019/08/08/drag-and-drop-file-upload-in-vuejs
  export default {
    name: 'v3FileUpload',
    mixins: [ v3Mixin ],
    components: {
      v3StepHeading,
      v3ButtonNext,
      v3miniValidate
      
    },
    data() {
      return {
        files: [],
        fileMetadata: [],
        target: null,
        pathSelection: 0,
        paths: [
          { 
            text: 'Single file',
            icon: 'mdi-file-outline',
            value: 'single'
          },
          { 
            text: 'Seperate training and generalization testing files',
            icon: 'mdi-file-outline',
            value: 'train-test'
          },
          // { 
          //   text: 'Multiple mixed data files needing combined',
          //   icon: 'mdi-file-multiple-outline',
          //   value: 'other'
          // },          
        ]
      }
    },
    props: {
      stepNumber: {
        type: Number || String
      },
      stepTitle: {
        type: String
      },
      currentStep: {
        type: Number
      },
      
    },
    watch: {
      pathSelection() {
        this.files = []
        this.target = null
      },

      files(current) {
        //Todo: figure out how to do this so it doesn't run on all files when new added

        console.log(current)
        let errorFiles = []
        this.files.forEach((item) => {
          console.log(item.type)
          if (item.type != 'text/csv') {
            errorFiles.push(item)
          }
        })
        errorFiles.forEach(f => {
          let r = this.files.indexOf(f)
          this.files.splice(r, 1)
        })
        if (errorFiles.length > 0) {
          let message = 'Some of your files were rejected due to an unsupported file format. '
          this.$store.commit('snackbarMessageSet', {color: 'red', message})
        }

        



        this.fileMetadata = []

        let promises = []
        this.files.forEach(file => {
          promises.push(storeParamFile(file))
        })
        Promise.all(promises).then(result => {
          result.forEach(r => {
              //front end override of file typing if one file
              if ([0, 2].includes(this.pathSelection)) {
                r.type = 'combined'
              }
              else if ([1].includes(this.pathSelection)) {
                r.type = ''
              }              
              this.fileMetadata.push(r)
          })
        })
        this.update()
      }
    },
    computed: {
      showAddFile() {
        switch (this.paths[this.pathSelection].value) {
          case 'single':
            return this.files.length <1

          case 'train-test':
            return this.files.length < 2

          default:
            return true
        }

      },
      trainTestFilesMatchError() {
        if (this.pathSelection == 1 && this.files.length == 2) {

            return this.fileMetadata[0].type == this.fileMetadata[1].type && this.fileMetadata[0].type != ''

        } 
        else {
          return false
        }

      },



      
      complete() {
        let advancedStep = this.currentStep > this.stepNumber
        advancedStep

        let hasTarget = this.target != null
        
        let twoFileValidation = true
        if (this.pathSelection == 1) {
          twoFileValidation = this.fileMetadata.length == 2
          this.fileMetadata.forEach(f => {
            if (f.type == '' || f.type == null) {
              twoFileValidation = false
            }
          })

        }

        return (hasTarget && twoFileValidation && !this.trainTestFilesMatchError)
      },
      allowMultipleFiles() {
        if (this.pathSelection != null) {
          return ['train-test', 'other'].includes(this.paths[this.pathSelection].value) ? true : false
        }
        else {
          return true
        }
      },
      filteredFileTypes() {
        //based on selected pathway
        if (this.pathSelection != null) {
          switch (this.paths[this.pathSelection].value) {
            case 'single':
              return this.mxfileTypes.filter(t => t.value == 'combined')
            case 'train-test':
              return this.mxfileTypes.filter(t => t.value == 'train' || t.value == 'test')
            case 'other':
              return this.mxfileTypes.filter(t => t.value == 'combined')
            default:
              return this.mxfileTypes
          }
        }
        else {
          return this.mxfileTypes
        }
      },



  
    },
    methods: {
      resetComponent() {
        this.files = []
        this.fileMetadata = []
        this.target = null
        this.pathSelection = 0     
      },
      update() {
        this.$emit('update')
      },
      next() {
        this.$emit('next', {
          fileMetadata: this.fileMetadata,
          target: this.target
        })
      },
      setPath(path) {
        this.pathSelection = path
        this.update()
      },
      clickAddFile(e) {
        for (let file of e.target.files) {
          this.files.push(file)
        }      
        this.$refs.fileClick.value = ''
      },
  
      addFile(e) {
        let droppedFiles = e.dataTransfer.files;
        if(!droppedFiles) return;
        // this tip, convert FileList to array, credit: https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
        ([...droppedFiles]).forEach(f => {
          this.files.push(f)
        });
  


  

      },
      removeFile(file){
        this.files = this.files.filter(f => {
          return f != file;
        });
      },
    }
  }
  </script>
  <style scoped>
  .path-selection {
    color: white;
    background-color: #1976d2;
    height:130px; 
    border-radius: 10px       
  }
  .path-no-selection {
    color: black;
    height:130px; 
    border: 1px solid #d3d3d3; 
    border-radius: 10px    
  }  

  #indent-text {
      margin-left: 1.8em;
      text-indent: -1.8em;
  }
  </style>
  