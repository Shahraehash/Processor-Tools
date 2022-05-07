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
        <input type="file" ref="fileClick" multiple="multiple" style="display: none"/>
      </div>
    </div>
    <v-card flat outlined class="pa-3 my-2" v-for="(file, index) in files" :key="index">
      <v-row dense v-if="fileMetadata[index]">
        <v-col cols="6">
          <v-icon>mdi-file</v-icon>
          {{ file.name }}
        </v-col>

        <v-col cols="5">
          Columns: {{fileMetadata[index].columns}}
          | Rows: {{fileMetadata[index].rows}}
        </v-col>
        <v-col cols="1" class="text-right">
          <v-btn icon @click="removeFile(file)" title="mdi-close">X</v-btn>
        </v-col>
      </v-row>
    </v-card>

    <div class="mt-10" v-if="fileMetadata[0]">
      <div class="my-3">
        Pick your target column.
      </div>
      <v-select 
        v-model="target" 
        dense 
        outlined 
        :items="fileMetadata[0].fields"
        @change="targetChanged"
        ></v-select>
    </div>
    <div class="text-right" v-if="this.target !=null && files.length > 0">
      <v-btn
        class="primary"
        :disabled="complete"
        @click="emitFileArray"
        rounded
        text
        dark
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
      target: null,
      complete: false,
      input: null,
    }
  },
  props: [
    'stepNumber',
    'stepTitle',
  ],
  watch: {
    files() {
      this.fileMetadata = []
      this.complete = false
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
    }
  },
  mounted() {
    this.input = this.$el.querySelector('input[type=file]');
    this.input.addEventListener('change', () => this.clickAddFile())
  },
  methods: {
    clickAddFile() {
      for (let file of this.input.files) {
        this.files.push(file)
      }
    },
    addFile(e) {
      let droppedFiles = e.dataTransfer.files;
      if(!droppedFiles) return;
      // this tip, convert FileList to array, credit: https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
      ([...droppedFiles]).forEach(f => {
        this.files.push(f);
      });
    },
    removeFile(file){
      this.files = this.files.filter(f => {
        return f != file;
      });
    },
    emitFileArray() {
      if (this.files.length > 0) {
        this.$emit('files', {files: this.files, target: this.target})
        this.complete = true
      }
    },
    targetChanged() {
      this.complete = false
    }
  }
}
</script>
