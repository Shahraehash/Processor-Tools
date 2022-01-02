<template>
  <div outlined class="ma-1 pa-1">
    <div class="overline mb-2">
      {{fileName}}
    </div>
    <v-layout class="ml-5">
      <v-row>
        <v-col cols="6" >
          <!-- <v-select
            outlined
            dense
            label="Data Set Type"
            v-model="fileObject.dataSet"
            :items="$store.state.dataSet"
            item-text="name"
            item-value="value"
          ></v-select> -->
          <v-file-input
            v-model="fileObject.file"
            prepend-icon="mdi-file"
            chips
            truncate-length="100"
            outlined
            :disabled="fileObject.dataSet == null"
            :label="fileName"
            @change="fileChanged"
          ></v-file-input>
        </v-col>
        <v-col cols="6" class="text-center">
          <v-progress-circular color="blue" size="50" width="10" v-if="fileObject.uploading" indeterminate></v-progress-circular>
          <DataValidation
            class="mt-n3"
            :fileData="fileObject.fileMetadata"
            :dataType="fileObject.dataSet"
            :maxRows="maxRows"
            :maxFeatures="maxFeatures"
            @dataValid="fileValidationSet"
          />
        </v-col>
      </v-row>
    </v-layout>
    <v-card
      hover
      class="ma-5"
      v-if="fileObject.fileMetadata"
      flat outlined
      >
      <div class="pa-3" @click="showTable = !showTable">
        <v-btn icon tile color=""><v-icon>mdi-chart-bar</v-icon></v-btn>
        Data Descriptions
        <span v-if="!showTable">(click to expand)</span>

        <v-icon v-if="!showTable">mdi-chevron-down</v-icon>
        <v-icon v-if="showTable">mdi-chevron-up</v-icon>
      </div>



          <v-data-table
            v-if="showTable"
            :headers="[
              {text: 'Column', value:'feature'},
              {text: 'Count', value:'count'},
              {text: 'Mean', value:'mean'},
              {text: 'STDEV', value:'std'},
              {text: 'Min', value:'min'},
              {text: '25%', value:'25%'},
              {text: '50%', value:'50%'},
              {text: '75%', value:'75%'},
              {text: 'Max', value:'max'},
              {text: 'Skew', value:'skew'},
              ]"
            :items="fileObject.fileMetadata.describe"
            class="elevation-1"
          >
          </v-data-table>

    </v-card>
  </div>


</template>
<script>
import DataValidation from '@/components/DataValidation'

export default {
  name: 'FileUploadSingle',
  components: {
    DataValidation
  },
  props: [
    'stepNumber', //StepHeading component
    'stepTitle', //StepHeading component
    'fileObject',
    'fileName',
    'maxRows',
    'maxFeatures'
  ],
  data() {
    return {
      showTable: false
    }
  },
  methods: {
    fileChanged(file) {
      if (file != null) {
        this.fileObject.dataFileUpload()
      }
      else {
        this.$emit('noFile')
      }
    },
    //Receives $emit from DataValidation component
    fileValidationSet(validation) {
      this.fileObject.fileValidation = validation
    }
  }
}
</script>
