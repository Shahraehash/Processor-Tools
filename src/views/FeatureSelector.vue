<template>
  <v-container>
    <MenuBar
      title="Feature Selector"
      icon="mdi-select-all"
      description="This tool allows you to find the most important features in your data."
      @reset="resetStep1"
    />
    <StepFileUploadMultiple
      stepNumber="1"
      stepTitle="File Upload"
      :file0="file0"
      :file1="file1"
      @hasSecondFile="hasSecondFile"
    />
    <StepTargetSelection
      v-if="stepNumber >= 2"
      stepNumber="2"
      stepTitle="Select Target"
      :fileObject="file0"
      nextStepFunction="generateCorrelation"
      nextStepParam="correlation"
      nextStepButtonText="Generate Correlation"
    />
    <StepFindCorrelation
      v-if="stepNumber >= 3"
      stepNumber="3"
      stepTitle="Find Correlations"
      :fileObject="file0"
      @nextStep="buildFiles"
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

export default {
  name: 'FeatureSelector',
  components: {
    MenuBar,
    StepFileUploadMultiple,
    StepTargetSelection,
    StepFindCorrelation
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
      step4Loading: false,
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
      else if (this.file0.fileMetadata != null && this.secondFile == true && this.file1.fileMetadata != null ) {
        return true
      }
      else {
        return false
      }
    },
    showStep3() {
      if (this.file0.target != null && this.file0.correlation != null) {
        return true
      }
      else {
        return false
      }
    },
    showStep4() {
      return false
    }


  },
  methods: {
    setStepState(e, val) {
      console.log(e, val)
    },
    resetStep1() {
      this.file0 = CustObjs.newFileObject()
      this.file1 = null
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
    buildFiles() {
      let promises = [this.file0.buildCorrelationFiles()]

      if (this.secondFile) {
        //duplicate removal list
        this.file1.target = this.file0.target
        this.file1.correlationFeatureRemovalList = this.file0.correlationFeatureRemovalList
        //add to promise for file processing
        promises.push(this.file1.buildCorrelationFiles())
      }

      //Data is saved on individual objects. This is just to confirm all operations complete.
      this.step4Loading = true
      Promise.all(promises).then((response) => {
        this.step4Loading = false
        console.log(response)
        FileDownload(this.file0.correlationOutputFiles.output_file, this.file0.fileOutputName + '.csv')
        if (this.file0.correlationOutputFiles.missing_count > 0) {
          FileDownload(this.file0.correlationOutputFiles.missing_file, this.file0.fileOutputName + '_missing_data.csv')
        }
        if (this.secondFile){
          FileDownload(this.file1.correlationOutputFiles.output_file, this.file1.fileOutputName + '.csv')
          if (this.file1.correlationOutputFiles.missing_count > 0) {
            FileDownload(this.file1.correlationOutputFiles.missing_file, this.file1.fileOutputName + '_missing_data.csv')
          }

        }
      })
    }

  }
}
</script>
