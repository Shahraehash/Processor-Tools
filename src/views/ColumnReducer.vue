<template>
  <v-container outlined>
    <MenuBar
      :title="$store.state.tools[$options.name].title"
      :icon="$store.state.tools[$options.name].icon"
      :description="$store.state.tools[$options.name].description"
      @reset="resetStep1"
    />

    <StepFileUploadMultiple
      stepNumber="1"
      stepTitle="File Upload"
      :file0="file0"
      :file1="file1"
      :maxRows="file0.defaultMaxRows"
      :maxFeatures="file0.defaultMaxFeatures"
      @hasSecondFile="hasSecondFile"
      @noFile0="resetStep1"
      @noFile1="resetSecondFileStep1"
    />
    <StepTargetSelection
      v-if="stepNumber >= 2"
      stepNumber="2"
      stepTitle="Select Target"
      :fileObject="file0"
      nextStepFunction="generateCorrelation"
      nextStepParam="confirmStep2"
      nextStepButtonText="Go to Column Selection"
      @resetStep="resetStep2"
      @nextStepState="confirmStep2Set"
    />

    <StepColumnReducerSelection
      v-if="stepNumber >= 3"
      stepNumber="3"
      stepTitle="Column Selection"
      :fileObject="file0"
      @changedStepData="resetStep4"
      @nextStep="buildFiles"
    />

    <StepFileOutput
      v-if="stepNumber >= 4"
      stepNumber="4"
      stepTitle="Output Files"
      :file0="file0"
      :file1="file1"
      :loadingFileData="step4Loading"
      outputFilesGroup='columnReducerOutputFiles'
      @saveFiles="saveFiles"
    />





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



  </v-container>

</template>
<script>
//packages
import axios from 'axios'
import FileDownload from 'js-file-download'

//support code
import CustObjs from '@/CustomObjects.js'

//components
import StepFileUploadMultiple from '@/components/steps/StepFileUploadMultiple'
import StepTargetSelection from '@/components/steps/StepTargetSelection'
import StepColumnReducerSelection from '@/components/steps/StepColumnReducerSelection'
import StepFileOutput from '@/components/steps/StepFileOutput'




import MenuBar from '@/components/MenuBar'

export default {
  name: 'ColumnReducer',
  components: {
    StepFileUploadMultiple,
    StepTargetSelection,
    StepColumnReducerSelection,
    StepFileOutput,




    MenuBar
  },
  data() {
    return {

      file0: null,
      file1: null,
      secondFile: null,
      confirmStep2: false,
      confirmStep3: false,
      step4Loading: false,
      fileSuffix: '_col_reduce',



      miloMetadata: null,
      miloDataLoading: false,




      miloColumns: [],
      miloDialog: false,
    }
  },
  created() {
    this.file0 = CustObjs.newFileObject()
    this.file1 = null
  },
  computed: {

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
      if (this.file0.fileMetadata != null
            && this.secondFile == false
            && this.file0.fileValidation.bool

          ) {
        return true
      }
      else if (this.file0.fileMetadata != null
                && this.secondFile == true
                && this.file1 != null
                && this.file1.fileMetadata != null
                && this.file0.fileValidation.bool
                //value is possibly read too fast after creation
                && this.file1.fileValidation != null
                && this.file1.fileValidation.bool == true
              ) {
        return true
      }
      else {
        return false
      }
    },
    showStep3() {
      if (this.file0.target != null && this.confirmStep2) {
        return true
      }
      else {
        return false
      }
    },
    showStep4() {
      if (this.confirmStep3) {
        return true
      }
      else {
        return false
      }
    }
  },
  methods: {
    buildFiles() {
      this.confirmStep3 = true
      let promises = [this.file0.buildColumnReducerFiles()]

      //add suffix
      this.file0.customFileOutputSuffix(this.fileSuffix)

      if (this.secondFile) {
        //duplicate removal list
        this.file1.target = this.file0.target
        this.file1.columnReducerSelectedColumns = this.file0.columnReducerSelectedColumns

        //add fileSuffix
        this.file1.customFileOutputSuffix(this.fileSuffix)
        //add to promise for file processing
        promises.push(this.file1.buildColumnReducerFiles())
      }

      //Data is saved on individual objects. This is just to confirm all operations complete.
      this.step4Loading = true
      Promise.all(promises).then((response) => {
        this.step4Loading = false
        console.log(response)

      })
    },













    resetStep1() {
      this.file0 = CustObjs.newFileObject()
      this.file1 = null
      this.secondFile = null
      this.resetStep2()
    },
    resetSecondFileStep1() {
      this.file1 = CustObjs.newFileObject()
      this.resetStep2()
    },
    resetStep2() {
      this.file0.target = null
      this.confirmStep2 = false
      this.resetStep3()
    },
    resetStep3() {
      this.file0.columnReducerSelectedColumns = []
      this.file0.columnReducerErrorColumns = []
      if (this.file1 != null) {
        this.file1.target = null
        this.file1.columnReducerSelectedColumns = []
        this.file1.columnReducerErrorColumns = []
      }
      this.resetStep4()
    },
    resetStep4() {
      this.confirmStep3 = false
      this.step4Loading = false
      this.file0.columnReducerOutputFiles = null

      if (this.file1 != null) {
        this.file0.columnReducerOutputFiles = null
      }
    },

    hasSecondFile(state) {
      this.secondFile = state
      if (state) {
        this.file1 = CustObjs.newFileObject()
      }
      else {
        this.file1 = null
      }
    },
    confirmStep2Set(state) {
      this.confirmStep2 = state
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
        axios.post('/preprocessor_api/column_reducer/milo_file_upload', formData, {
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

    saveFiles(exportSettings) {
      console.log(exportSettings)
      FileDownload(this.file0.columnReducerOutputFiles.output_file, this.file0.fileOutputName + '.csv')
      if (this.file0.columnReducerOutputFiles.missing_count > 0 && exportSettings.exportMissingRows) {
        FileDownload(this.file0.columnReducerOutputFiles.missing_file, this.file0.fileOutputName + '_missing_data.csv')
      }
      if (this.secondFile){
        FileDownload(this.file1.columnReducerOutputFiles.output_file, this.file1.fileOutputName + '.csv')
        if (this.file1.columnReducerOutputFiles.missing_count > 0 && exportSettings.exportMissingRows) {
          FileDownload(this.file1.columnReducerOutputFiles.missing_file, this.file1.fileOutputName + '_missing_data.csv')
        }
      }
      //Show download UI
      this.$store.commit('FileProcessingDialogOpenSet', true)
    }



  }


}
</script>
<style>


</style>
