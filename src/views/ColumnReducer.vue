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
      nextStepFunction="generateColumnReduction"
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
  </v-container>
</template>
<script>
//packages
import FileDownload from 'js-file-download'
import JSZip from 'jszip'
//support code
import CustObjs from '@/CustomObjects.js'

//components
import MenuBar from '@/components/MenuBar'
import StepFileUploadMultiple from '@/components/steps/StepFileUploadMultiple'
import StepTargetSelection from '@/components/steps/StepTargetSelection'
import StepColumnReducerSelection from '@/components/steps/StepColumnReducerSelection'
import StepFileOutput from '@/components/steps/StepFileOutput'

export default {
  name: 'ColumnReducer',
  components: {
    MenuBar,
    StepFileUploadMultiple,
    StepTargetSelection,
    StepColumnReducerSelection,
    StepFileOutput,
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
    //File operations
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
    saveFiles(exportSettings) {

      let safari = CustObjs.isSafari()
      let zip = new JSZip();
      console.log('isSafari',safari)

      safari ? zip.file(this.file0.fileOutputName + '.csv', this.file0.columnReducerOutputFiles.output_file) : FileDownload(this.file0.columnReducerOutputFiles.output_file, this.file0.fileOutputName + '.csv')

      if (this.file0.columnReducerOutputFiles.missing_count > 0 && exportSettings.exportMissingRows) {
        safari ? zip.file(this.file0.fileOutputName + '_missing_data.csv', this.file0.columnReducerOutputFiles.missing_file) : FileDownload(this.file0.columnReducerOutputFiles.missing_file, this.file0.fileOutputName + '_missing_data.csv')
      }
      if (this.secondFile){
        safari ? zip.file(this.file1.fileOutputName + '.csv', this.file1.columnReducerOutputFiles.output_file) : FileDownload(this.file1.columnReducerOutputFiles.output_file, this.file1.fileOutputName + '.csv')
        if (this.file1.columnReducerOutputFiles.missing_count > 0 && exportSettings.exportMissingRows) {
          safari ? zip.file(this.file1.fileOutputName + '_missing_data.csv', this.file1.columnReducerOutputFiles.missing_file) : FileDownload(this.file1.columnReducerOutputFiles.missing_file, this.file1.fileOutputName + '_missing_data.csv')
        }
      }
      //Show download UI
      if (safari) {
        zip.generateAsync({type:"blob"})
        .then(function(content) {
            // Force down of the Zip file
            FileDownload(content, "column_reducer_combined_files.zip");
        });
      }
      this.$store.commit('FileProcessingDialogOpenSet', true)
    },
    //State Progression
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
    //State Resetting
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
    }
  }
}
</script>
<style>


</style>
