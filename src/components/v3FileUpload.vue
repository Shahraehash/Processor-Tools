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
    <!-- If no files yet -->
      <div 
        v-if="files.length == 0" 
        class="text-center"
        style="border: 5px dashed #d3d3d3; border-radius: 10px; padding: 20px;"
        >
        <div >
          Drag and drop your CSV file(s) into this box or click the file icon below to select from systemc dialog.
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
        multiple="multiple" 
        @change="clickAddFile($event)" 
        style="display: none" 
        accept='.csv'
        />

    <!-- If have files -->

      <v-row dense>
        <v-col cols="4"
          v-for="(file, index) in files" 
          :key="index"
          >

          <v-card 
            flat 
            outlined 
            class="pa-3 my-2 training-style" 
            v-bind:style="{ 'border-color': mxfileTypeColor(fileMetadata[index].type)}"
            >
            

                
                  <v-row>
                    <v-col cols="11">
                      <div style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;">
                        <v-icon>mdi-file</v-icon>
                        {{ file.name }}
                      </div>

                    </v-col>
                    <v-col cols="1" class="ml-n5 mt-n2">
                      <v-btn icon @click="removeFile(file)" title="mdi-close"><v-icon color="primary">mdi-close</v-icon></v-btn>
                    
                    </v-col>

                  </v-row>
                
                
                <div>
                  <v3miniValidate :valid="true" />
                  {{fileMetadata[index].size.rows}} rows
                </div>
                <div>
                  <v3miniValidate :valid="true" />
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
                    
                    v-model="fileMetadata[index].type" 
                    class="ma-2 mt-7" 
                     
                    label="Data Type" 
                    :items="mxfileTypes" 
                    item-text="text" 
                    item-value="value"
                    @change="update()"
                    >
                    <template v-slot:selection="{ item, index }">
                      <v-chip small v-if="index === 0" :color="mxfileTypeColor(item.value)" dark>
                        <span>{{ item.text }}</span>
                      </v-chip>
     
 
                    </template>

                  </v-select>
                </div>
              



          </v-card>          
          
        </v-col>
        <v-col cols="4" v-if="files.length > 0">
          <v-card flat style="margin: 10px; padding: 100px 0;">
            <div class="text-center mr-3" @click="$refs.fileClick.click()">
            <div class="overline">Add addtional file</div> 
            <v-btn icon
              
              >
              <v-icon large>mdi-plus-circle-outline</v-icon>
              </v-btn>
          </div>

          </v-card>

        </v-col>
      </v-row>



  


      <!-- Pick Target -->
      <div class="mt-10" v-if="fileMetadata[0]">
        <div class="my-3">
          Pick your target column.
        </div>
        <v-row>
          <v-col cols="6">
            <v-select 
              v-model="target" 
              dense 
              outlined 
              :items="fileMetadata[0].names.colsReverse"
              @change="update()"
              ></v-select>          
          </v-col>
        </v-row>
  
      </div>


      <div class="text-right" v-if="files.length > 0">
        <v3ButtonNext 
        @next="next"
        :disabled="currentStep > stepNumber - 1 || !target"
        text="Done adding data files"
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
        fileIds: [], //ids of files in the database, temporary
        fileMetadata: [],
        target: null
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

      files(current, previous) {
        //Todo: figure out how to do this so it doesn't run on all files when new added

        if (current.length >= previous.length) {
          this.fileMetadata = []
          this.files.forEach(file => {
          storeParamFile(file).then(r => this.fileMetadata.push(r))
          })          

        }

        this.update()
      }
    },
    computed: {
      complete() {
        return true
      }


  
    },
    methods: {
      //import
      //defined
      update() {
        this.$emit('update')
      },
      next() {
        this.$emit('next', {
          fileMetadata: this.fileMetadata,
          target: this.target
        })
      },


      clickAddFile(e) {
        for (let file of e.target.files) {
          this.files.push(file)
        }      
        this.$refs.fileClick.value = ''
      },
  
      addFile(e) {
        let errorFiles = []
        let droppedFiles = e.dataTransfer.files;
        if(!droppedFiles) return;
        // this tip, convert FileList to array, credit: https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
        ([...droppedFiles]).forEach(f => {
          if (f.type == 'text/csv') {
            this.files.push(f)
          }        
          else {
            errorFiles.push(f.name)
          }             
            
        });
  
        if (errorFiles.length > 0) {
          let message = 'Some of your files were rejected due to an unsupported file format: '
          message += errorFiles.join(', ')
          this.$store.commit('snackbarMessageSet', {color: 'red', message})
  
        }
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
  #indent-text {
      margin-left: 1.8em;
      text-indent: -1.8em;
  }

  .training-style {
    box-sizing: border-box;
    border-width: 5px;
    border-radius: 10px;
  }
  </style>
  