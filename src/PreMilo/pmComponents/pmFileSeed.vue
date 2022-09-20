<template>

    <v-card 
      outlined 
      flat 
      class="ma-3 pa-5" 
      @drop.prevent="addFile" 
      @dragover.prevent
      >
    <!-- If no files yet -->
      <div 
        v-if="files.length == 0" 
        class="text-center"
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
      <v-card 
        flat 
        outlined 
        class="pa-3 my-2" 
        v-for="(file, index) in files" 
        :key="index"
        >
        <v-row dense v-if="fileMetadata[index]">
          <v-col cols="6">
            <v-icon>mdi-file</v-icon>
            {{ file.name }}
            
          </v-col>
          <v-spacer></v-spacer>
          <v-col cols="1">{{fileMetadata[index].rows}}x {{fileMetadata[index].columns}}</v-col>
          <v-col cols="1" class="text-right">
          <v-btn icon @click="removeFile(file)" title="mdi-close"><v-icon color="primary">mdi-close</v-icon></v-btn>
        </v-col>          
        </v-row>
      </v-card>

  
      <div class="text-right mr-3" v-if="files.length > 0">
        <v-btn icon
          @click="$refs.fileClick.click()"
          >
          <v-icon>mdi-plus-circle-outline</v-icon>
          </v-btn>
      </div>
  
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
              :items="fileMetadata[0].fields"
              @change="targetChange"
              ></v-select>          
          </v-col>
        </v-row>
  
      </div>
      <div class="text-right" v-if="this.target !=null && files.length > 0">
        <v-btn
          class="primary"
          rounded
          text
          dark
          :disabled="disableNext"
          @click="$emit('nextStep')"
          >
          Evaluate Files
        </v-btn>
      </div>
    </v-card>
  </template>
  <script>
  //packages
  // import Papa from 'papaparse'
  import axios from 'axios'
  //support code
  


  //components
  
  //Inspired by: https://www.raymondcamden.com/2019/08/08/drag-and-drop-file-upload-in-vuejs
  export default {
    name: 'pmFileSeed',
    components: {
      
    },
    data() {
      return {
        files: [],
        fileMetadata: [],
        input: null,
        target: null,
        backendFileData: null,
        imputeWarning: {
          rows: 2000,
          cols: 50
        }
      }
    },
    props: [
    ],
    watch: {

      files() {
        this.fileMetadata = []
        this.files.forEach(file => {
          this.storeFile(file).then(r => {
            return this.paramsFile(r.storageId)
          }).then(r => {
            this.fileMetadata.push(r)
          })

        })
        this.filesChange() 
      }
    },
    mounted() {
  
    },
    methods: {

      async storeFile(file) {
          var formData = new FormData();
          formData.append('files', file);

          const response = await axios.post('/preprocessor_api/integrated/store', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          return response.data //returns key value pair with file name and storage key
      },   
      
      async paramsFile(storageId) {

          let json = {storageId}

          const response = await axios.post('/preprocessor_api/integrated/params', json, {
            headers: {
              'Content-Type': 'application/json',
            }
          })
          return response.data
      },         

  
      reset() {
        this.files = []
        this.fileMetadata = []
        this.target = null
        this.input = null
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
  </style>
  