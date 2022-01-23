<template>
  <v-container>

    <MenuBar
      :title="$store.state.tools[$options.name].title"
      :icon="$store.state.tools[$options.name].icon"
      :description="$store.state.tools[$options.name].description"
      @reset="resetStep1"
    />

      <!-- STEP 1 -->
      <v-card

        outlined
        class="ma-3 pa-5"
      >
        <StepHeading
          stepNumber="1"
          stepTitle="Select Data File"
        />
        <div>
          <!-- Training -->
          <v-card outlined class="ma-5 pa-3">
            <div class="overline ml-5 mb-3">
              Single Data File
            </div>

            <v-layout class="ml-5">
              <v-row>
                <v-col cols="6" >

                  <v-file-input v-model="file" prepend-icon="mdi-file" chips truncate-length="100" outlined label="Data File"  @change="fileUpload"></v-file-input>
                </v-col>
                <v-col cols="6" class="text-center">
                  <v-progress-circular color="blue" size="50" width="10" v-if="fileDataLoading" indeterminate></v-progress-circular>
                  <DataValidation
                    class="mt-n3"
                    :fileData="fileData"
                    dataType="combined"
                    @dataValid="fileValidationData"
                    :maxRows="100000"
                    :maxFeatures="2000"
                  />
                </v-col>
              </v-row>
            </v-layout>
          </v-card>

          <ErrorMessage v-if="fileDataValid ? fileDataValid.alerts.textData : false" type="error" text="Milo cannot use columns with non-numerical data. We advise fixing this before proceeding." />

        </div>
      </v-card>

      <!-- STEP 2 -->
      <v-card
        v-if="showStep2"
        outlined
        class="ma-3 pa-5"
      >
        <StepHeading
          stepNumber="2"
          stepTitle="Select Target Column"
        />
        <div>

          <v-row>
              <v-col cols="6">
                <v-select
                  clearable
                  outlined
                  label="Target Column"
                  prepend-icon="mdi-bullseye"
                  v-if="fileData"
                  v-model="targetColumn"
                  :items='fileData.column_names'
                  @change="determineClassMetadata"
                ></v-select>
              </v-col>
            </v-row>
            <v-alert
              dense
              text
              type="warning"
              v-if="class0nanSize >0 || class1nanSize > 0"
            >
              Rows with missing data will be dropped during processing.
              <div v-if="class0nanSize >0">
                <span v-if="class0nanSize == 1">For class 0: {{class0nanSize}} row is excluded.</span>
                <span v-if="class0nanSize > 1">For class 0: {{class0nanSize}} rows are excluded. </span>
                (
                <span style="text-decoration: line-through">{{class0size}}</span>
                <v-icon color="orange">mdi-arrow-right</v-icon>
                {{class0size - class0nanSize}}
                )
              </div>
              <div v-if="class1nanSize >0">
                <span v-if="class1nanSize == 1">For class 1: {{class1nanSize}} row is excluded.</span>
                <span v-if="class1nanSize > 1">For class 1: {{class1nanSize}} rows are excluded.</span>
                (
                <span style="text-decoration: line-through">{{class1size}}</span>
                <v-icon color="orange">mdi-arrow-right</v-icon>
                {{class1size - class1nanSize}}
                )
              </div>


            </v-alert>
            <div style="width:100%" >
              <div
                class="distrobution-box"
                v-bind:style="{
                  background: '#2196F3',
                  width: class0width + '%'
                  }"
                >
                <div
                  v-bind:style="{
                    opacity: 0.3,
                    background:'white',
                    width: class0nanPercent + '%',
                    position:'absolute',
                    left:'16px',
                    bottom:'15px'
                    }"
                  class="distrobution-box"
                >
                </div>
                <p class="pa-0 ma-0">
                  Class 0 ({{class0percent}}%)
                </p>
                <p class="pa-0 ma-0" v-if="class0nanSize == 0">
                  N={{class0size}}
                </p>
                <p class="pa-0 ma-0" v-if="class0nanSize > 0">
                  <span style="text-decoration: line-through">{{class0size}}</span>
                  <v-icon color="white">mdi-arrow-right</v-icon>
                  {{class0size - class0nanSize}}
                </p>
              </div>
              <div
                class="distrobution-box"
                v-bind:style="{
                  background: '#009688',
                  width: class1width + '%'
                  }"
                >
                <div
                  v-bind:style="{
                    opacity: 0.3,
                    background:'white',
                    width: class1nanPercent + '%',
                    position:'absolute',
                    right:'16px',
                    bottom:'15px'
                    }"
                  class="distrobution-box"
                >
                </div>
                <p class="pa-0 ma-0">
                  Class 1 ({{class1percent}}%)
                </p>
                <p class="pa-0 ma-0" v-if="class1nanSize == 0">
                  N={{class1size}}
                </p>
                <p class="pa-0 ma-0" v-if="class1nanSize > 0">
                  <span style="text-decoration: line-through">{{class1size}}</span>
                  <v-icon color="white">mdi-arrow-right</v-icon>
                  {{class1size - class1nanSize}}
                </p>
              </div>

              <div class="distrobution-box" v-bind:style="{ background: '#d3d3d3', width: placeholderSlot + '%' }">Data Distrobution Displayed After Selection</div>
            </div>
            <ErrorMessage
              v-if="minSampleSizeError"
              type="error"
              :text="'To use this tool, each class must have a an N greater than ' + minSampleSize "
              />



        </div>
      </v-card>

      <!-- STEP 3 -->
      <v-card
        outlined
        class="ma-3 pa-5"
        v-if="showStep3"
      >
        <StepHeading
          stepNumber="3"
          stepTitle="Select Split"
        />
        <div>

          <ClassGroupBar
            v-if="classMetadata"
            :metadata="classMetadata"
            @calculation="receiveClassGroupBarData"
          />

        </div>
      </v-card>

      <!-- STEP 4 -->
      <v-card
        v-if="showStep4"
        outlined
        class="ma-3 pa-5"
      >
        <StepHeading
          stepNumber="4"
          stepTitle="Output Files"
        />
        <div>
          <div>

            <v-switch v-model="outputSettings.includeRowIndex" label="Include row index in output"></v-switch>
          </div>

          <v-row>
            <v-col cols="6">
              <v-text-field
                v-model="outputFiles.training"
                outlined
                dense
                label="Training Data File Name"
                suffix=".csv"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                v-model="outputFiles.testing"
                outlined
                dense
                label="Testing Data File Name"
                suffix=".csv"
              ></v-text-field>
            </v-col>
          </v-row>

          <div >
            <div class="overline">Additional File Outputs</div>
            <v-row>
              <v-col cols="6"
                v-if="splitData ? splitData.extraCount > 0 : false"

              >

                <v-switch
                label="Export unused data."
                v-model="outputSettings.extraFile"
                ></v-switch>

                <v-text-field
                  outlined
                  dense
                  label="Extra Data File"
                  suffix=".csv"
                  v-model="outputFiles.extra"
                  v-if="outputSettings.extraFile"
                ></v-text-field>
              </v-col>

              <v-col cols="6"

                v-if="fileData.nan_count > 0"
              >
                <div>
                  <v-switch
                  label="Export rows with missing data."
                  v-model="outputSettings.nanFile"
                  ></v-switch>
                </div>
                <v-text-field
                  outlined
                  dense
                  label="Rows with Missing Data File"
                  suffix=".csv"
                  v-model="outputFiles.nan"
                  v-if="outputSettings.nanFile"
                ></v-text-field>
              </v-col>

            </v-row>

          </div>
          <div class="text-right">
            <v-btn
              dark
              rounded
              float="right"
              color="primary"
              @click="processFiles()"
            >
              Create Files
              <v-icon class="pl-2">mdi-file</v-icon>
            </v-btn>
          </div>
        </div>
      </v-card>
  </v-container>

</template>
<script>
import axios from 'axios'
import FileDownload from 'js-file-download'
import DataValidation from '@/components/DataValidation'
import StepHeading from '@/components/StepHeading'
import ErrorMessage from '@/components/ErrorMessage'
import ClassGroupBar from '@/components/ClassGroupBar'
import MenuBar from '@/components/MenuBar'

export default {
  name: 'TrainTestSplit',
  components: {
    DataValidation,
    StepHeading,
    ErrorMessage,
    ClassGroupBar,
    MenuBar,

  },
  data() {
    return {
      e1: 1,

      file: null,
      fileData: null,
      fileDataValid: null,
      fileDataLoading: false,

      prevalenceOption: 0,

      //STEP 2
      targetColumn: null,
      targetColumnList: [],
      classMetadata: null,
      //class computed
      class0size: 0,
      class0percent: 0,
      class0nanSize: 0,
      class0nanPercent: 0,
      class0width: 0,
      class1size: 0,
      class1percent: 0,
      class1nanSize: 0,
      class1nanPercent: 0,
      class1width: 0,

      placeholderSlot: 100,

      splitData: null,

      outputFiles: {
        training: null,
        testing: null,
        nan: null,
        extra:null
      },
      outputSettings: {
        includeRowIndex: false,
        nanFile: false,
        extraFile: false,
      },


      minSampleSize: 25,
    }
  },
  computed: {
    //Control Which Steps Shows,
    showStep2() {
      if (
        this.fileData != null
        && (this.fileDataValid ? this.fileDataValid.bool : false) // if data field exists
      ) {
        return true
      } else {
        return false
      }

    },
    showStep3() {
      if (
        this.showStep2
        && this.targetColumn != null
        && !this.minSampleSizeError
      ) {
        return true
      } else {
        return false
      }

    },
    showStep4() {
      if (
        this.showStep3
      ) {
        return true
      } else {
        return false
      }

    },
    //Errors
    minSampleSizeError() {
      if (this.classMetadata != null) {
        if (this.classMetadata.class_counts[0] < this.minSampleSize || this.classMetadata.class_counts[1] < this.minSampleSize) {
          return true
        }

        else {
          return false
        }
      }
      return false
    }

  },
  methods: {
    resetStep1() {
      this.file = null
      this.fileData = null
      this.fileDataValid = null
      this.targetColumnList = []
      this.resetStep2()

    },
    resetStep2() {
      this.targetColumn = null
      this.classMetadata = null
      this.class0size = 0
      this.class0percent = 0
      this.class0nanSize = 0
      this.class0nanPercent = 0
      this.class0width = 0
      this.class1size = 0
      this.class1percent = 0
      this.class1nanSize = 0
      this.class1nanPercent = 0
      this.class1width = 0
      this.placeholderSlot = 100

      this.resetStep3()
    },
    resetStep3() {
      console.log('reset step 3')
      this.splitData = null

    },

    fileUpload(file) {
      if (file != null) {
        //this method uploads form data
        var formData = new FormData();

        //UI
        this.fileDataLoading = true

        //file name data stored in X-file header of post request
        formData.append("file", file);
        axios.post('/preprocessor_api/shared/data_file_upload', formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            'X-filename': file.name,
            'X-filegroup': 'train_test_split'

          }
        }).then(result => {
          this.fileDataLoading = false
          //file data stored in data field of result
          this.fileData = result.data

          //set target column options
          this.targetColumnList = this.fileData.column_names.reverse()

        }).catch(() => {
          this.fileDataLoading = false
          this.$store.commit('snackbarMessageSet', {
            color: 'red lighten-1',
            message: 'Error processing file.'
          })
          this.resetStep1()
        })
      }
      else {
        this.fileDataLoading = false
        this.resetStep1()
      }

    },
    fileValidationData(result){
      console.log(result)
      this.fileDataValid = result
    },


    determineClassMetadata(field){
      if (field != null) {
        let data = {
          target_column: this.targetColumn,
          storage_id: this.fileData.storage_id
        }
        return axios.post('train_test_split/metadata', data, {
          headers: {
          'Content-Type': 'application/json',
          }
        }).then(result => {
          //Parse JSON in subobjects
          this.classMetadata = result.data
          console.log(result.data)
          this.classMetadata.class_counts = JSON.parse(this.classMetadata.class_counts)

          //If missing data, process the counts
          if (this.classMetadata.nan_class_counts != null) {
            this.classMetadata.nan_class_counts = JSON.parse(this.classMetadata.nan_class_counts)
          }

          //Calculated values and UI parameters
          //Step 2
          this.calculateMetadataMetrics() //for Step 2 bar
          //Step 4
          this.makeFileNames()


        }).catch(() => {
          this.$store.commit('snackbarMessageSet', {
            color: 'red lighten-1',
            message: 'Invalid column selection. Values are not binary.'
          })
          this.resetStep2()

        })
      }
      else {
        this.resetStep2()
      }

    },
    receiveClassGroupBarData(data) {
      this.splitData = data
    },

    makeFileNames() {
      let fn = this.file.name.trim()
      fn = fn.replace('.csv', '')
      fn = fn.trim()
      this.outputFiles.training = fn + '_training'
      this.outputFiles.testing = fn + '_testing'
      this.outputFiles.extra = fn + '_extra'
      this.outputFiles.nan = fn + '_missing_data'
    },
    processFiles() {
      let data = {
        target_column: this.targetColumn,
        storage_id: this.fileData.storage_id,
        majority_class: this.classMetadata.majority_class,

        training_class_sample_size: this.splitData.trainingClassSize, //Not matched to output
        prevalence_option: this.splitData.prevalenceOption, //0 = use all data, 1 = maintain initail prevalence
        extra: this.splitData.extraCount, // extra data used in maintaining inital prevalence

        include_index: this.outputSettings.includeRowIndex

      }
      console.log(data)

      //UI elements
      this.$store.commit('FileProcessingDialogOpenSet', true)
      this.$store.commit('FileProcessingDialogLoadingSet', true)

      return axios.post('train_test_split/process', data, {
        headers: {
        'Content-Type': 'application/json',
        }
      }).then(response => {
        console.log(response)

        //UI elements
        this.$store.commit('FileProcessingDialogLoadingSet', false)

        //File elements
        //Change file name if index included in main output
        if (this.outputSettings.includeRowIndex) {

          FileDownload(response.data.training, this.outputFiles.training + '_with_index.csv')
          FileDownload(response.data.testing, this.outputFiles.testing + '_with_index.csv')
        }
        else {
          FileDownload(response.data.training, this.outputFiles.training + '.csv')
          FileDownload(response.data.testing, this.outputFiles.testing + '.csv')
        }



        if (this.outputSettings.extraFile) {
          FileDownload(response.data.extra, this.outputFiles.extra + '.csv')
        }
        if (this.outputSettings.nanFile) {
          try {
            FileDownload(response.data.nan, this.outputFiles.nan + '.csv')
          }
          catch(err) {
            console.log('error')
          }

        }
      })

    },
    calculateMetadataMetrics() {
      //Initial Class Sizes
      this.class0size = this.classMetadata.class_counts[0]
      this.class1size = this.classMetadata.class_counts[1]

      //Prevalence of Each Class - used for display values but not widths
      this.class0percent = Math.round(1000 * (this.classMetadata.class_counts[0] / this.classMetadata.total_count)) / 10
      this.class1percent = Math.round(1000 * (this.classMetadata.class_counts[1] / this.classMetadata.total_count)) / 10

      //Set the actual widths - copying variables was not working properly so duplicated
      this.class0width = Math.round(1000 * (this.classMetadata.class_counts[0] / this.classMetadata.total_count)) / 10
      this.class1width = Math.round(1000 * (this.classMetadata.class_counts[1] / this.classMetadata.total_count)) / 10

      // Adjust UI if low prevalence
      if (this.class0width < 20) {
        this.class0width = 20
        this.class1width = 80
      }

      if (this.class1width < 20) {
        this.class1width = 20
        this.class0width = 80
      }

      //Hide Placeholder
      this.placeholderSlot = 0

      //Show dropped data if necessary
      if (this.classMetadata.nan_class_counts != null) {
        this.class0nanSize = this.classMetadata.nan_class_counts[0]
        this.class0nanPercent = Math.round(1000 * (this.classMetadata.nan_class_counts[0] / this.classMetadata.class_counts[0])) / 10

        this.class1nanSize = this.classMetadata.nan_class_counts[1]
        this.class1nanPercent = Math.round(1000 * (this.classMetadata.nan_class_counts[1] / this.classMetadata.class_counts[1])) / 10
      }
    },

    // calculateMetadataMetrics() {
    //   this.class0size = this.classMetadata.class_counts[0]
    //   this.class1size = this.classMetadata.class_counts[1]
    //   this.class0percent = Math.round(1000 * (this.classMetadata.class_counts[0] / this.classMetadata.total_count)) / 10
    //   this.class1percent = Math.round(1000 * (this.classMetadata.class_counts[1] / this.classMetadata.total_count)) / 10
    //   this.placeholderSlot = 0
    //   if (this.classMetadata.nan_class_counts != null) {
    //     this.class0nanSize = this.classMetadata.nan_class_counts[0]
    //     this.class0nanPercent = Math.round(1000 * (this.classMetadata.nan_class_counts[0] / this.classMetadata.class_counts[0])) / 10
    //
    //     this.class1nanSize = this.classMetadata.nan_class_counts[1]
    //     this.class1nanPercent = Math.round(1000 * (this.classMetadata.nan_class_counts[1] / this.classMetadata.class_counts[1])) / 10
    //   }
    // },
  }

}
</script>
<style>
.distrobution-box {
  padding-top:16px;
  height: 80px;
  transition: width 0.5s;
  display: inline-block;
  text-align: center;
  color: white;
  overflow: hidden;
}
.title-box {
  padding-top:5px;
  height: 30px;
  transition: width 0.5s;
  display: inline-block;
  text-align: center;
  color: white;
  overflow: hidden;
}

.loaders-transition {
  transition: 0.5s;
}


</style>
