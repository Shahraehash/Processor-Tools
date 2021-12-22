<template>
  <v-container>
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
      nextStepButtonText="Generate Correlation"
      @resetStep="resetStep2"
      @nextStepState="confirmStep2Set"
    />
    <StepFindCorrelation
      v-if="stepNumber >= 3"
      stepNumber="3"
      stepTitle="Find Correlations"
      :fileObject="file0"
      @changedFeatureRemoval="resetStep4"
      @nextStep="buildFiles"
    />
    <StepFileOutput
      v-if="stepNumber >= 4"
      stepNumber="4"
      stepTitle="Output Files"
      :file0="file0"
      :file1="file1"
      :loadingFileData="step4Loading"
      outputFilesGroup='correlationOutputFiles'
      @saveFiles="saveFiles"
    />

  </v-container>

</template>

<script>
//packages
import FileDownload from 'js-file-download'

//support code
import CustObjs from '@/CustomObjects.js'

//components
import MenuBar from '@/components/MenuBar'
import StepFileUploadMultiple from '@/components/steps/StepFileUploadMultiple'
import StepTargetSelection from '@/components/steps/StepTargetSelection'
import StepFindCorrelation from '@/components/steps/StepFindCorrelation'
import StepFileOutput from '@/components/steps/StepFileOutput'

export default {
  name: 'Colinearity',
  components: {
    MenuBar,
    StepFileUploadMultiple,
    StepTargetSelection,
    StepFindCorrelation,
    StepFileOutput
  },
  props: [],
  created() {
    this.file0 = CustObjs.newFileObject()
    this.file1 = null
  },
  data() {
    return {
      file0: null,
      file1: null,
      secondFile: null,
      confirmStep2: false,
      confirmStep3: false,
      step4Loading: false,
      fileSuffix: '_corr_removal'
    }
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
      if (this.file0.fileMetadata != null && this.secondFile == false) {
        return true
      }
      else if (this.file0.fileMetadata != null && this.secondFile == true && this.file1 != null && this.file1.fileMetadata != null ) {
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
    setStepState(e, val) {
      console.log(e, val)
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
      this.file0.correlation = null
      this.confirmStep2 = false
      this.resetStep3()
    },
    resetStep3() {
      this.file0.correlationFeatureRemovalList = []
      if (this.file1 != null) {
        this.file1.target = null
        this.file1.correlationFeatureRemovalList = []
      }
      this.resetStep4()
    },
    resetStep4() {
      this.confirmStep3 = false
      this.step4Loading = false
      this.file0.correlationOutputFiles = null

      if (this.file1 != null) {
        this.file0.correlationOutputFiles = null
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
    buildFiles() {
      this.confirmStep3 = true
      let promises = [this.file0.buildCorrelationFiles()]

      //add suffix
      this.file0.customFileOutputSuffix(this.fileSuffix)

      if (this.secondFile) {
        //duplicate removal list
        this.file1.target = this.file0.target
        this.file1.correlationFeatureRemovalList = this.file0.correlationFeatureRemovalList

        //add fileSuffix
        this.file1.customFileOutputSuffix(this.fileSuffix)
        //add to promise for file processing
        promises.push(this.file1.buildCorrelationFiles())
      }

      //Data is saved on individual objects. This is just to confirm all operations complete.
      this.step4Loading = true
      Promise.all(promises).then((response) => {
        this.step4Loading = false
        console.log(response)

      })
    },
    saveFiles(exportSettings) {
      console.log(exportSettings)
      FileDownload(this.file0.correlationOutputFiles.output_file, this.file0.fileOutputName + '.csv')
      if (this.file0.correlationOutputFiles.missing_count > 0 && exportSettings.exportMissingRows) {
        FileDownload(this.file0.correlationOutputFiles.missing_file, this.file0.fileOutputName + '_missing_data.csv')
      }
      if (this.secondFile){
        FileDownload(this.file1.correlationOutputFiles.output_file, this.file1.fileOutputName + '.csv')
        if (this.file1.correlationOutputFiles.missing_count > 0 && exportSettings.exportMissingRows) {
          FileDownload(this.file1.correlationOutputFiles.missing_file, this.file1.fileOutputName + '_missing_data.csv')
        }
      }
    }

  }
}
</script>
