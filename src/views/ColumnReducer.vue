<template>
  <v-container outlined>
    <MenuBar
      :title="$store.state.tools[$options.name].title"
      :icon="$store.state.tools[$options.name].icon"
      :description="$store.state.tools[$options.name].description"
      @reset="resetStep1Training"
    />


    <v-card
      v-bind:style="{'opacity': setTransparencyFromStepProgress(1)}"
      outlined
      class="ma-3 pa-5"
    >
      <StepHeading
        stepNumber="1"
        stepTitle="Select Data File(s)"
      />
      <div>
        <!-- Training -->
        <v-card outlined class="ma-5 pa-3">
          <div class="overline ml-5 mb-3">
            Training File
          </div>

          <v-layout class="ml-5">
            <v-row>
              <v-col cols="6" >

                <v-file-input v-model="trainingFileData" prepend-icon="mdi-file" chips truncate-length="100" outlined label="Training Data File"  @change="dataFileUploadTraining"></v-file-input>
              </v-col>
              <v-col cols="6" class="text-center">
                <v-progress-circular color="blue" size="50" width="10" v-if="trainingDataLoading" indeterminate></v-progress-circular>
                <DataValidation
                  class="mt-n3"
                  :fileData="trainingMetadata"
                  dataType="training"
                  @dataValid="dataValidationTrainingData"
                />
              </v-col>
            </v-row>
          </v-layout>
        </v-card>



        <Decision
          v-if="trainingMetadata != null"
          :decision="testingFile"
          @decide="setTestingFileState"
          message="Do you have a second generalization testing file?"
          trueVal="Yes"
          falseVal="No"
        />



        <v-card outlined class="ma-5 pa-3" v-if="testingFile == true">
          <div class="overline ml-5 mb-3">
            Generalization Testing File
          </div>
          <v-layout class="ml-5" >
            <v-row>
              <v-col cols="6" >

                <v-file-input v-model="testingFileData" prepend-icon="mdi-file" chips truncate-length="100" outlined label="Testing Data File"  @change="dataFileUploadTesting"></v-file-input>
              </v-col>
              <v-col cols="6" class="text-center">
                <v-progress-circular color="blue" size="50" width="10" v-if="testingDataLoading" indeterminate></v-progress-circular>
                <DataValidation
                  class="mt-n3"
                  :fileData="testingMetadata"
                  dataType="testing"
                  @dataValid="dataValidationTestingData"
                />
              </v-col>
            </v-row>
          </v-layout>
        </v-card>

        <v-card outlined class="ma-5 pa-3" v-if="testingFile == true && testingMetadata != null">
          <div class="overline ml-5 mb-3">
            Cross-File Validation
          </div>
          <v-layout class="ml-5" >
            <v-row>
              <v-col cols="12" >
                <div v-if="dataColumnsMatch != null" class="body-1">
                  <div>
                    <div v-if="dataColumnsMatch.numberOfColumnsMatch">
                      <v-icon color="green" >mdi-check-circle</v-icon> Number of Columns Match Between Files
                    </div>
                    <div v-if="!dataColumnsMatch.numberOfColumnsMatch">
                      <v-icon color="red" >mdi-alert-circle</v-icon> Number of Columns Differ Between Files
                    </div>

                  </div>
                  <div>
                    <div v-if="dataColumnsMatch.columnNamesMatch">
                      <v-icon color="green" >mdi-check-circle</v-icon> Column Names Match Between Files
                    </div>
                    <div v-if="!dataColumnsMatch.columnNamesMatch">
                      <v-icon color="red" >mdi-alert-circle</v-icon> Column Names Differ Between Files

                      <div class="pl-10 pb-5">
                        <div>
                          Columns in Test File Missing from Training:
                          <v-chip outlined v-for="(i, j) in dataColumnsMatch.inTestNotTrain" :key="j">{{i}}</v-chip>
                        </div>
                        <div>
                          Columns in Training File Missing from Training:
                          <v-chip outlined v-for="(i, j) in dataColumnsMatch.inTrainNotTest" :key="j">{{i}}</v-chip>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </v-col>
            </v-row>
          </v-layout>
        </v-card>
      </div>
    </v-card>


    <v-card
      v-bind:style="{'opacity': setTransparencyFromStepProgress(2)}"
      outlined
      class="ma-3 pa-5"
      v-if="showStep2"
    >
      <StepHeading
        stepNumber="2"
        stepTitle="Target Selection"
      />
      <div>
        <p>
          Identify the column containing your target variable to ensure it is maintain in the output.
        </p>
        <v-layout class="ma-5">

          <v-row wrap>
            <v-col cols="6">
              <v-autocomplete
                clearable
                outlined
                label="Target Column"
                v-model="target"
                :items="targetColumnList"
                @change="targetColumnChanged"


              ></v-autocomplete>
              <!-- v-model="target"
              label="Target Column"

              @change="targetColumnChanged" -->
            </v-col>

          </v-row>
        </v-layout>
        <div v-if="target != null" class="body-1">
          <div v-if="targetValid == true" >
            <v-icon color="green" >mdi-check-circle</v-icon> Valid target column.

          </div>
          <div v-if="targetValid == false" >
            <v-icon color="red" >mdi-alert-circle</v-icon> The selected target column is not valid. There must be two unique values.
          </div>
        </div>

      </div>
    </v-card>


    <v-card
      v-bind:style="{'opacity': setTransparencyFromStepProgress(3)}"
      outlined
      class="ma-3 pa-5"
      v-if="showStep3"
    >
      <StepHeading
        stepNumber="3"
        stepTitle="Column Selection"
      />
      <div>
        <p>Click below to selected columns or paste a comma seperated list of columns to be outputted. <br /> You can also <a @click="miloDialog = true">import from a MILO results "report.csv" file</a>.</p>
        <v-layout class="ma-5">

          <v-row wrap>


            <v-col cols="12">

              <v-combobox clearable v-model="selectedColumns" multiple chips class="ml-8" :items="nontargetColumnList"  outlined label="Selected Columns" @change="splitPasted()"></v-combobox>
              <div>
              </div>
              <div v-if="selectedColumns.length > 0" class="body-1">
                <div>
                  <v-icon color="green" >mdi-check-circle</v-icon> {{selectedColumns.length}} columns selected.
                </div>
              </div>
              <div v-if="errorColumns != null">
                <div v-if="errorColumns.length > 0">
                  <v-alert class="mt-3" text type="error" dismissible dense>
                    <span>The following column<span v-if="errorColumns.length > 1">s</span> are invalid:</span>
                    <v-chip class="ml-2" small dark color="red lighten-3" v-for="(item,key) in errorColumns" :key="key">{{item}}</v-chip>
                  </v-alert>


                </div>
              </div>

              <p>

              </p>
            </v-col>

          </v-row>
        </v-layout>

      </div>
      <div class="text-right" v-if="selectedColumns.length > 0">
        <v-btn
          v-if="confirmColumnSelection == false"
          color="primary"
          rounded
          @click="proceedToStep4()"
        >
          Confirm Column Selection
        </v-btn>
      </div>
    </v-card>


    <v-card
      v-bind:style="{'opacity': setTransparencyFromStepProgress(4)}"
      outlined
      class="ma-3 pa-5"
      v-if="showStep4"
    >
      <StepHeading
        stepNumber="4"
        stepTitle="Output Files"
      />
      <div>
        <v-layout>
          <v-row>
            <v-col cols="6">
              <v-card class="px-3 py-1 mt" flat outlined>
                <div class="overline">
                  Output Summary
                </div>
                <div>
                  <div v-if="fileOutputs == null">
                    <v-progress-circular color="blue" size="50" width="10" indeterminate></v-progress-circular>

                  </div>
                  <div v-if="fileOutputs != null">
                    <div>
                      Total Columns: {{selectedColumns.length + 1}} (including target)
                    </div>
                    <div>
                      Feature Columns: {{selectedColumns.length}} of {{nontargetColumnList.length}} original
                    </div>
                    <div>
                      Target Column: {{target}}
                    </div>
                    <div>
                      Training Rows Total: {{trainingMetadata.rows}}
                    </div>
                    <div>
                      Training Rows Used: {{trainingMetadata.rows - fileOutputs.training_missing_count}}
                    </div>
                    <div>
                      Training Rows Missing Data: {{fileOutputs.training_missing_count}}
                    </div>
                    <div v-if="testingMetadata != null">
                      Testing Rows Total: {{testingMetadata.rows}}
                    </div>
                    <div v-if="testingMetadata != null">
                      Testing Rows Used: {{testingMetadata.rows - fileOutputs.testing_missing_count}}
                    </div>
                    <div v-if="testingMetadata != null">
                      Testing Rows Missing Data: {{fileOutputs.testing_missing_count}}
                    </div>

                  </div>

                </div>

              </v-card>

            </v-col>
            <v-col cols="6">
              <div>
                <v-text-field
                  label="Training File Output"
                  v-model="trainingOutputFilename"
                  suffix=".csv"
                  outlined
                  dense
                >
                </v-text-field>
              </div>

              <div>
                <v-text-field
                  v-if="testingMetadata != null"
                  label="Testing File Output"
                  v-model="testingOutputFilename"
                  suffix=".csv"
                  outlined
                  dense
                >
                </v-text-field>
              </div>
              <div class="overline">Additional File Outputs</div>
              <div>
                <v-switch
                  label="Export rows with missing data."
                  v-model="exportNanRows"


                ></v-switch>
              </div>
              <div class="text-right">
                <v-btn
                  color="primary"
                  rounded
                  @click="buildFiles()"
                  v-if="fileOutputs != null"
                >
                  Build Files
                </v-btn>

              </div>
            </v-col>

          </v-row>
        </v-layout>
      </div>
    </v-card>

    <v-dialog max-width="700" v-model="miloDialog">
      <v-card flat class="pa-3 pb-6">
        <v-card-title>
          <p>Import Columns from MILO Results "report.csv" File</p>
          <v-spacer></v-spacer>
          <v-btn @click="miloDialog = false" icon flat class="mt-n5">
            <v-icon medium>mdi-close</v-icon>
          </v-btn>

        </v-card-title>
        <v-card-text class="mx-0 py-0">
          <v-file-input prepend-icon="mdi-file" chips truncate-length="200" outlined label="MILO Data File"  @change="miloFileUpload"></v-file-input>
          <v-progress-linear v-if="miloDataLoading" indeterminate></v-progress-linear>
          <v-spacer></v-spacer>

          <div>
            <div class="ml-8 mb-3" >Select columns based on the feature selector method. Note: Random Forest options are not included because each is run specific. Also, any method that does not reduced the number of columns is not included.</div>
            <v-select v-if="miloMetadata" :items="miloMetadata" v-model="miloColumns" class="ml-8"  outlined  label="Feature Selector Method"></v-select>
            <div>
              <v-chip small color="grey lighten-2" v-for="(item, key) in miloColumns" :key="key">{{item}}</v-chip>

            </div>
          </div>



        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="mr-2" rounded dark color="primary" @click="setMiloColumns">Select Columns</v-btn>

        </v-card-actions>



      </v-card>

    </v-dialog>

    <FileProcessingDialog :isOpen="fileProcessingDialog" :loading="fileProcessingInProgress" />





  </v-container>

</template>
<script>
import axios from 'axios'
import _ from 'underscore'
import FileDownload from 'js-file-download'
import DataValidation from '@/components/DataValidation'
import StepHeading from '@/components/StepHeading'
import Decision from '@/components/Decision'
import FileProcessingDialog from '@/components/FileProcessingDialog'
import MenuBar from '@/components/MenuBar'

export default {
  name: 'ColumnReducer',
  components: {
    DataValidation,
    StepHeading,
    Decision,
    FileProcessingDialog,
    MenuBar
  },
  data() {
    return {
      file: '',
      loading: false,
      serverData: null,
      trainingFileData: null,
      trainingMetadata: null,
      trainingDataLoading: false,
      trainingDataValid: true,


      testingFile: null, //boolean to control flow
      testingFileData: null, //link to file
      testingMetadata: null, //link to server meta data extacted
      testingDataLoading: false,
      testingDataValid: true,

      miloMetadata: null,
      miloDataLoading: false,

      targetColumnList: null,
      nontargetColumnList: null,
      target: null,
      targetValid: null,


      toggle: null,
      selectedColumns: [],
      errorColumns: null,
      confirmColumnSelection: false,

      removeNanRows: true, //not exposed to user
      exportNanRows: true,
      trainingOutputFilename: '',
      testingOutputFilename: '',
      fileOutputs: null,
      fileProcessingDialog: false,
      fileProcessingInProgress: true,


      miloColumns: [],
      miloDialog: false,
    }
  },
  sockets: {
    connect: function () {
        console.log('socket connected')
    },
    customEmit: function (data) {
        this.serverData = data
        this.loading = false
    }
  },
  computed: {
    dataColumnsMatch() {
      if (this.trainingMetadata != null && this.testingMetadata != null) {
        let numberOfColumnsMatch = this.trainingMetadata.columns == this.testingMetadata.columns

        let inTrainNotTest = _.difference(this.trainingMetadata.column_names, this.testingMetadata.column_names)
        let inTestNotTrain = _.difference(this.testingMetadata.column_names, this.trainingMetadata.column_names)

        let columnNamesMatch = inTestNotTrain.length == 0 && inTrainNotTest.length == 0
        return {numberOfColumnsMatch, columnNamesMatch, inTrainNotTest, inTestNotTrain}
      }
      else {
        return null
      }
    },
    stepNumber() {
      if (this.showStep4) {
        return 4
      }
      else if (this.showStep3) {
        return 3
      }
      else if (this.showStep2) {
        return 2
      }
      else {
        return 1
      }
    },
    showStep2() {
      if (
        this.trainingMetadata != null
        && this.testingFile == false
      ) {
        return true
      }
      else if (
        this.trainingMetadata != null
        && this.testingFile == true
        && this.testingMetadata != null
        //Ensure the files are compatible and no errors
        && (this.dataColumnsMatch.numberOfColumnsMatch && this.dataColumnsMatch.columnNamesMatch)
      ) {
        return true

      }
      else {
        return false
      }
    },
    showStep3() {
      if (this.showStep2
          && this.target != null
          && this.targetValid == true
        ) {
        return true
      }
      else {
        return false
      }

    },
    showStep4() {
      if (this.showStep3
          && this.selectedColumns.length > 0
          && this.confirmColumnSelection
      ) {
        return true
      }
      else {
        return false
      }

    }
  },
  methods: {
    dataFileUploadTraining(file) {
      if (file != null) {
        this.trainingDataLoading = true

        this.dataFileUpload(file, 'training_data')
        .then(response => {
          this.trainingMetadata = response.data
          this.trainingDataLoading = false
          this.trainingOutputFilename = this.trainingFileData.name.replace('.csv', '') + '_reduced'
          let identity = (x) => x
          this.targetColumnList = this.trainingMetadata.column_names.map(identity)
          this.targetColumnList = this.targetColumnList.reverse()
        })
      }
      else {
        this.resetStep1Training()
      }
    },
    dataFileUploadTesting(file) {
      if (file != null) {
        this.testingDataLoading = true

        this.dataFileUpload(file, 'testing_data')
        .then(response => {
          this.testingMetadata = response.data
          this.testingDataLoading = false
          this.testingOutputFilename = this.testingFileData.name.replace('.csv', '') + '_reduced'
        })
      }
      else {
        this.testingMetadata = null
      }
    },
    dataFileUpload(file, type) {
      if (file != null) {
        //this method uploads form data
        var formData = new FormData();

        //file name data stored in X-file header of post request
        formData.append("file", file);
        return axios.post('/data_file_upload', formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            'X-filename': file.name,
            'X-filegroup': type
          }
        }).then(response => {
          return response
        }).catch(() => {
          this.$store.commit('snackbarMessageSet', {
            color: 'red lighten-1',
            message: 'Error processing file.'
          })
          // this.resetStep1()
        })
      }
      else {
        return 'nothing'
        //this.resetStep1()
      }

    },
    dataValidationTrainingData(result) {
      this.trainingDataValid = result
    },
    dataValidationTestingData(result) {
      this.testingDataValid = result
    },
    proceedToStep4() {
      this.confirmColumnSelection = true
      window.scrollTo(0,document.body.scrollHeight);
      this.processFiles()
    },

    processFiles() {
      this.fileOutputs = null
      let data = {}
      data.training_storage_id = this.trainingMetadata.storage_id
      data.testing_storage_id = this.testingMetadata != null ? this.testingMetadata.storage_id : null
      data.selected_columns = this.selectedColumns
      data.target_column = this.target
      data.remove_nan_rows = this.removeNanRows

      return axios.post('/column_reducer/process', data, {
        headers: {
        'Content-Type': 'application/json',
        }
      }).then(response => {
        this.fileOutputs = response.data
      })
    },
    buildFiles() {
      //File elements
      FileDownload(this.fileOutputs.training, this.trainingOutputFilename + '.csv')

      //If Second Testing File
      if (this.fileOutputs.testing != 'null') {
        FileDownload(this.fileOutputs.testing, this.testingOutputFilename + '.csv')
      }

      //If missing data files
      if (this.fileOutputs.training_missing != 'null' && this.exportNanRows) {
        FileDownload(this.fileOutputs.training_missing, this.trainingOutputFilename + '_missing_data.csv')
      }

      if (this.fileOutputs.testing_missing != 'null' && this.exportNanRows) {
        FileDownload(this.fileOutputs.training_missing, this.testingOutputFilename + '_missing_data.csv')
      }

    },

    resetStep1Training() {
      this.trainingFileData = null
      this.trainingMetadata = null
      this.trainingDataValid = true
      this.targetColumnList = null
      this.nontargetColumnList = null
      this.trainingOutputFilename = ''
      this.testingFile = null
      this.fileProcessingDialog = false

      this.resetStep1Testing()
      this.resetStep2()

    },
    resetStep1Testing() {
      // this.testingFile = null
      this.testingFileData = null
      this.testingMetadata = null
      this.testingDataValid = true
      this.testingOutputFilename = ''
    },
    resetStep2() {
      this.target = null
      this.targteValid = null
      this.resetStep3()
    },
    resetStep3() {
      this.selectedColumns = []
      this.errorColumns = null
      this.confirmColumnSelection = false
      this.resetStep4()
    },
    resetStep4() {
      this.confirmColumnSelection = false
    },

    splitPasted() {
      //Split Pasted Text
      this.selectedColumns.forEach((item, index) => {
        if (item.includes(',')) {
          console.log('comma detected', item, index)
          let result = item.split(',')
          result.map(s => s.trim());
          this.selectedColumns.splice(index, 1, result)
        }
      })
      this.selectedColumns = this.selectedColumns.flat()

      //Validate Columns
      this.errorColumns = []
      this.selectedColumns.forEach(item => {
        if (!this.nontargetColumnList.includes(item)) {
          this.errorColumns.push(item)

        }
      })
      this.errorColumns.forEach(err => {
        let i = this.selectedColumns.indexOf(err)
        this.selectedColumns.splice(i, 1)
      })

      if (this.errorColumns.length == 0) {
        this.errorColumns = null
      }

      //Unique values only
      this.selectedColumns = _.uniq(this.selectedColumns)
      console.log(this.selectedColumns)

      //Reset step 4 when columns change
      this.resetStep4()


    },
    targetColumnChanged(value) {
      if (value == null) {
        this.resetStep2()
      }
      else {

        let payload = {
          target: this.target,
          storage_id: this.trainingMetadata.storage_id
        }

        axios.post('/validate/target_column', payload, {
            headers: {
            'Content-Type': 'application/json',
            'X-inbound': 'validation'
          }
        }).then(result => {
          this.targetValid = result.data.validation
        })


        this.nontargetColumnList = []
        this.trainingMetadata.column_names.forEach(item => {

          if (item != value) {

            this.nontargetColumnList.push(item)
          }
        })

      }

    },
    testEmit() {
      this.$socket.emit('custom')
      this.loading = true
    },

    miloFileUpload(file){
      if (file != null) {
        var formData = new FormData();
        this.miloDataLoading = true

        formData.append("file", file);
        axios.post('milo_file_upload', formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            'X-inbound': 'milo_file'
          }
        }).then(result => {
          this.miloMetadata = []
          let data = JSON.parse(result.data.result).selected_features
          for (let i in data) {
            this.miloMetadata.push({
              text: i,
              value: JSON.parse(data[i])
            })
          }
          this.miloDataLoading = false

        })
      }
      else {
        this.miloMetadata = null
        this.miloDataLoading = false
      }
    },
    setMiloColumns() {

      this.selectedColumns = this.miloColumns
      console.log(this.selectedColumns)
      this.miloDialog = false
    },

    //Support Functions

    //UI Functions
    setTransparencyFromStepProgress(step) {
      if (this.stepNumber > step) {
        return 0.7
      }
      else {
        return 1.0
      }
    },

    //Helper functions
    setTestingFileState(bool) {
      console.log(bool)
      this.testingFile = bool
    }


  }


}
</script>
<style>


</style>
