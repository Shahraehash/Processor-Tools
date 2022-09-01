<template>


  <v-card outlined flat class="ma-3 pa-5" @drop.prevent="addFile" @dragover.prevent>
    <StepHeading
      :stepNumber="stepNumber"
      :stepTitle="stepTitle"
    />
    <div v-if="files.length == 0" class="text-center">
      <div >Drag and drop your CSV file(s) into this box or click the file icon below to select from systemc dialog.</div>
      <div>
        <v-icon size="125" @click="$refs.fileClick.click()" color="grey lighten-1">
          mdi-file-upload-outline
        </v-icon>
        
      </div>
    </div>
    <!-- Hidden file upload -->
    <input type="file" ref="fileClick" multiple="multiple" @change="clickAddFile($event)" style="display: none" accept='.csv'/>

    <v-card flat outlined class="pa-3 my-2" v-for="(file, index) in files" :key="index">
      <v-row dense v-if="fileMetadata[index]">
        <v-col cols="6">
          <v-icon>mdi-file</v-icon>
          {{ file.name }}
        </v-col>

        <v-col cols="5">
         <div v-if="backendFileData">
            <div><v-icon class="mr-1">mdi-arrow-expand-horizontal</v-icon>{{backendFileData[index].params.columns}} columns</div>
            <div><v-icon class="mr-1">mdi-arrow-expand-vertical</v-icon>{{backendFileData[index].params.rows}} rows</div>
          
            <div>
              <v-icon color="green" v-if="backendFileData[index].params.nanCells == 0">mdi-check-circle</v-icon>
              <v-icon color="orange" v-else>mdi-alert-circle</v-icon>
              {{stylePercent(backendFileData[index].params.nanPercent)}}% of cells missing data ({{backendFileData[index].params.nanCells}} cells)
            </div>
            <div>
              <v-icon color="green" v-if="backendFileData[index].params.nanRows == 0">mdi-check-circle</v-icon>
              <v-icon color="orange" v-else>mdi-alert-circle</v-icon>
              {{backendFileData[index].params.nanRows}} row<span v-if="backendFileData[index].params.nanRows > 1">s</span> missing data 
            </div>
            <div id="indent-text" v-if="backendFileData[index].params.columns >= imputeWarning.cols || backendFileData[index].params.rows > imputeWarning.rows">
              <v-icon color="red" >mdi-alert-circle</v-icon>
              Based on the size of you dataset, imputing the missing values may take a signficant period of time.
            </div>                    
          </div>
        </v-col>
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
import Papa from 'papaparse'
//support code

//components
import StepHeading from '@/components/StepHeading'

//Inspired by: https://www.raymondcamden.com/2019/08/08/drag-and-drop-file-upload-in-vuejs
export default {
  name: 'StepFileDrop',
  components: {
    StepHeading
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
    'stepNumber',
    'stepTitle',
    'disableNext',
    'backendFileDataProp'

  ],
  watch: {
    backendFileDataProp() {
      console.log('backendMetadataProp changed')
      this.backendFileData = this.backendFileDataProp
    },
    files() {
      this.fileMetadata = []
      this.files.forEach(file => {
        Papa.parse(file, {header: true, complete: t => {
          let meta = t.meta
          meta.rows = t.data.length
          meta.columns = t.meta.fields.length
          meta.fields = meta.fields.reverse()
          meta.type = null
          this.fileMetadata.push(meta)
        }})
      })
      this.filesChange() 
    }
  },
  mounted() {

  },
  methods: {



    reset() {
      this.files = []
      this.fileMetadata = []
      this.target = null
      this.input = null
      this.backendData = null
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
    filesChange() {
      this.$emit('filesChange', this.files)
      this.target = null
    },
    targetChange() {
      this.$emit('targetChange', this.target)
    },
    evaluateMetadata() {
      this.$emit('evaluateMetadata')
    },
    stylePercent(value) {
      if (value >= 1) {
        return Math.round(value)
      }
      else if (value < 1 && value > 0) {
        return "<1"
      }
      else {
        return 0
      }

    }
  }
}
</script>
<style scoped>
#indent-text {
    margin-left: 1.8em;
    text-indent: -1.8em;
}
</style>
