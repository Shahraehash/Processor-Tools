<template>
  <v-container outlined>
    <v-card outlined class="ma-3 pa-3">
      <div >
        <v-row>
          <v-col cols="3">
            <v-btn icon @click="$router.push({name: 'Landing'})"><v-icon>mdi-arrow-left</v-icon></v-btn>
          </v-col>
          <v-col cols="6" class="text-center">
            <v-icon x-large>mdi-table-column-width</v-icon>
            <span class="title">Column Reducer Tool</span>
          </v-col>
          <v-col cols="3">
          </v-col>
        </v-row>
      </div>
      <v-card-text class="body-1">
        This tool allows to extract specific columns from your training and test data to experiment with further refinement of your model.
      </v-card-text>
    </v-card>

    <v-card outlined class="ma-3 pa-3 ">
      <v-card-title class="">
        Step 1 - Select Data File(s)
      </v-card-title>
      <v-card-text class="">

        <p>
          Select your training data file. You may also select a second testing data file.
        </p>
        <v-layout class="ma-5">
          <v-row>
            <v-col cols="6" >
              <v-file-input prepend-icon="mdi-file" chips truncate-length="100" outlined label="Training Data File"  @change="trainingFileUpload"></v-file-input>
              <span v-if="trainingMetadata != null">
                Columns: {{trainingMetadata.columns}} | Rows: {{trainingMetadata.rows}}
              </span>
            </v-col>
            <v-col cols="6">
              <v-file-input  prepend-icon="mdi-file" chips truncate-length="100" outlined label="Testing Data File (optional)" @change="testingFileUpload" :disabled="trainingMetadata == null"></v-file-input>
              <span  v-if="testingMetadata != null">
                Columns: {{testingMetadata.columns}} | Rows: {{testingMetadata.rows}}
              </span>
            </v-col>
          </v-row>
        </v-layout>

        <div v-if="dataColumnsMatch == null && trainingMetadata != null" class="body-1">
          <div>
            <v-icon color="green" >mdi-check-circle</v-icon> Valid Data File
          </div>
        </div>

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





      </v-card-text>


    </v-card>





    <v-card class="ma-3 pa-3" v-if="trainingMetadata">
      <v-card-title>Step 2 - Target Selection</v-card-title>
      <v-card-text >
        <p>
          Identify the column containing your target variable to ensure it is maintain in the output.
        </p>
        <v-layout class="ma-5">

          <v-row wrap>
            <v-col cols="6">
              <v-autocomplete clearable :items="targetColumnList" outlined v-model="target" label="Target Column" @change="targetColumnChanged"></v-autocomplete>
            </v-col>

          </v-row>
        </v-layout>
        <div v-if="target != null" class="body-1">
          <div>
            <v-icon color="green" >mdi-check-circle</v-icon> Valid Target Field
          </div>
        </div>
      </v-card-text>
    </v-card>

    <v-card class="ma-3 pa-3" v-if="target">
      <v-card-title>Step 3 - Column Selection</v-card-title>




      <p>Click below to selected columns or paste a comma seperated list of columns to be outputted. <br /> You can also <a @click="miloDialog = true">import from a MILO results "report.csv" file</a>.</p>
      <v-layout class="ma-5">

        <v-row wrap>


          <v-col cols="12">

            <v-combobox clearable v-model="selectedColumns" multiple chips class="ml-8" :items="nontargetColumnList"  outlined label="Selected Columns" @change="splitPasted()"></v-combobox>
            <div v-if="errorColumns == null && selectedColumns.length > 0" class="body-1">
              <div>
                <v-icon color="green" >mdi-check-circle</v-icon> Valid Column Selection
              </div>
            </div>
            <div v-if="errorColumns != null">
              <div v-if="errorColumns.length > 0">
                <v-icon color="red" >mdi-alert-circle</v-icon>
                <span>The following column<span v-if="errorColumns.length > 1">s</span> are invalid and have been removed from the list:</span>
                <v-chip small outlined v-for="(item,key) in errorColumns" :key="key">{{item}}</v-chip>
              </div>
            </div>

            <p>

            </p>
          </v-col>

        </v-row>
      </v-layout>

      <v-card-text >

      </v-card-text>
    </v-card>

    <v-card class="ma-3 pa-3" v-if="errorColumns == null && selectedColumns.length > 0">
      <v-card-title>Step 4 - Save Files</v-card-title>
      <v-card-text>
        <v-row>

          <v-col cols="3" class="mr-0 pr-1">
            <v-text-field v-model="trainingOutputFilename" label="Training Output" outlined></v-text-field>
          </v-col>
          <v-col cols="1" class="ml-0 pl-0 pt-7">
            <div class="body-1 black--text" >
              .csv
            </div>

          </v-col>


          <v-col cols="3" class="mr-0 pr-1">
            <v-text-field v-model="testingOutputFilename" label="Testing Output" outlined></v-text-field>
          </v-col>
          <v-col cols="1" class="ml-0 pl-0 pt-7">
            <div class="body-1 black--text" >
              .csv
            </div>

          </v-col>
        </v-row>
        <v-btn @click="finalFileRequests">Build Decks</v-btn>
        {{trainingMetadata}}




      </v-card-text>
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
          <v-spacer></v-spacer>

          <div>
            <div class="ml-8 mb-3" >Select columns based on the feature selector method.</div>
            <v-select v-if="miloMetadata" :items="miloMetadata" v-model="miloColumns" class="ml-8"  outlined  label="Feature Selector Method"></v-select>
            <div>
              {{miloColumns}}
            </div>
          </div>



        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="mr-2" rounded large dark color="grey darken-3" @click="setMiloColumns">Select Columns</v-btn>

        </v-card-actions>



      </v-card>

    </v-dialog>





  </v-container>

</template>
<script>
import axios from 'axios'
import _ from 'underscore'
import FileDownload from 'js-file-download'

export default {
  name: 'Home',
  data() {
    return {
      file: '',
      loading: false,
      serverData: null,
      trainingMetadata: null,
      testingMetadata: null,
      miloMetadata: null,
      targetColumnList: null,
      nontargetColumnList: null,
      target: null,
      toggle: null,
      selectedColumns: [],
      errorColumns: null,
      trainingOutputFilename: 'training_reduced',
      testingOutputFilename: 'testing_reduced',
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
  },
  methods: {
    resetStepOne() {

    },
    resetStepTwo() {

    },
    resetStepThree() {

    },
    resetStepFour() {

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


    },
    targetColumnChanged(value) {
      if (value == null) {
        this.nontargetColumnList = null
      }
      else {
        this.nontargetColumnList = []
        this.trainingMetadata.column_names.reverse().forEach(item => {

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
    trainingFileUpload(file){
      if (file != null) {
        var formData = new FormData();

        formData.append("file", file);
        axios.post('data_upload', formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            'X-inbound': 'training_data'
          }
        }).then(result => {
          this.trainingMetadata = result.data
          this.targetColumnList = this.trainingMetadata.column_names.reverse()
          this.trainingOutputFilename = file.name.replace('.csv','') + '_reduced'
        })
      }
      else {
        this.trainingMetadata = null
        this.trainingOutputFilename = ''
      }

    },
    testingFileUpload(file){
      if (file != null) {
        var formData = new FormData();
        console.log(file)

        formData.append("file", file);
        axios.post('data_upload', formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            'X-inbound': 'testing_data'
          }
        }).then(result => {
          this.testingMetadata = result.data
          this.testingOutputFilename = file.name.replace('.csv','') + '_reduced'
        })
      }
      else {
        this.testingMetadata = null
        this.testingOutputFilename = ''
      }
    },
    miloFileUpload(file){
      if (file != null) {
        var formData = new FormData();

        formData.append("file", file);
        axios.post('data_upload', formData, {
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
          console.log(this.miloMetadata)

        })
      }
      else {
        this.miloMetadata = null
      }
    },
    setMiloColumns() {
      this.selectedColumns = this.miloColumns
      this.miloDialog = false
    },
    finalFileRequests() {
      let finalColumns = []
      this.selectedColumns.forEach(column => {
        finalColumns.push(column)
      })
      finalColumns.push(this.target)

      let hasTestData = !this.testingMetadata == null

      let reductionData = {finalColumns, hasTestData}
      axios.post('column_reducer/build_files', reductionData, {
        headers: {
        'Content-Type': 'application/json',
      }

      })
      .then(() => {


        return axios.post('/column_reducer/training_reduced_file', {name: this.trainingOutputFilename}, {
          headers: {
          'Content-Type': 'application/json',
          }
        })

      }).then(response => {
        console.log(response)
        FileDownload(response.data, this.trainingOutputFilename + '.csv')

        if (this.testingMetadata != null) {
          return axios.get('/column_reducer/testing_reduced_file')
        }
      }).then(response => {
        if (this.testingMetadata != null) {
          FileDownload(response.data, this.testingOutputFilename + '.csv')
        }
      })


    }
  }


}
</script>
